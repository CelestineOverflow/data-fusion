import cv2
import pupil_apriltags as apriltag
import numpy as np
import scipy as sp
import json
from mjpeg_streamer import MjpegServer, Stream
import argparse
import threading
from zeroconf import (
    IPVersion,
    ServiceBrowser,
    ServiceStateChange,
    Zeroconf,
    ZeroconfServiceTypes,
)
import socket

imu_service_ip = "localhost"
imu_service_port = 6969
lock = threading.Lock() 

def on_service_state_change(zeroconf, service_type, name, state_change):
    global imu_service_ip, imu_service_port, lock
    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        print("Info from zeroconf.get_service_info: %r" % (info))
        with lock:  # Use the lock when updating global variables
            imu_service_ip = info.parsed_addresses()[0]
            imu_service_port = info.port

def create_udp_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_data_over_udp(sock, data, ip, port):
    try:
        # Directly check if the data dictionary is empty
        if not data:  # This will be True if data is an empty dictionary
            return  # Do nothing and return early
        
        # If data is not empty, convert it to JSON string
        json_data = json.dumps(data)
        sock.sendto(json_data.encode(), (ip, port))
        # print(f"Sent: {json_data}")
    except Exception as e:
        print(f"Error: {e}")



class Camera:
    def __init__(self, calibration_file_path, as_degrees=True):
        self.mtx, self.dist = self.load_calibration_file(calibration_file_path)
        self.detector = apriltag.Detector(families='tag36h11', nthreads=1, quad_decimate=1.0, quad_sigma=0.0, refine_edges=1, decode_sharpening=0.25, debug=0)
        self.as_degrees = as_degrees

    def load_calibration_file(self, calibration_file_path):
        with open(calibration_file_path, 'r') as infile:
            reconstruction = json.load(infile)
            mtx = np.array(reconstruction['mtx'])
            mtx = [mtx[0, 0], mtx[1, 1], mtx[0, 2], mtx[1, 2]]
            dist = np.array(reconstruction['dist'])
            return mtx, dist

    def detector_superimpose(self, img, tag_size=0.16):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detections = self.detector.detect(gray, estimate_tag_pose= True, camera_params=(self.mtx), tag_size=tag_size)
        data = {}
        data["camera"] = {}
        for d in detections:
            pose_data = d.pose_R, d.pose_t
            rvec, tvec = pose_data[0], pose_data[1]
            quaternion = sp.spatial.transform.Rotation.from_matrix(rvec).as_quat()
            rotation = sp.spatial.transform.Rotation.from_matrix(rvec).as_euler('xyz', degrees=self.as_degrees)
            x, y, z = rotation[0], rotation[1], rotation[2]
            cv2.circle(img, (int(d.center[0]), int(d.center[1])), 5, (0, 0, 255), -1)
            cv2.putText(img, str(d.tag_id), (int(d.center[0]), int(d.center[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            #draw angle and position of tag
            cv2.putText(img, "x: " + str(round(x, 2)), (int(d.center[0]), int(d.center[1]) + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(img, "y: " + str(round(y, 2)), (int(d.center[0]), int(d.center[1]) + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(img, "z: " + str(round(z, 2)), (int(d.center[0]), int(d.center[1]) + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(img, "t x: " + str(round(tvec[0][0], 2)), (int(d.center[0]), int(d.center[1]) + 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(img, "t y: " + str(round(tvec[1][0], 2)), (int(d.center[0]), int(d.center[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(img, "t z: " + str(round(tvec[2][0], 2)), (int(d.center[0]), int(d.center[1]) + 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            single_tag_data = {}
            single_tag_data["position"] = {}
            single_tag_data["position"]["x"] = tvec[0][0]
            single_tag_data["position"]["y"] = tvec[1][0]
            single_tag_data["position"]["z"] = tvec[2][0]
            single_tag_data["quaternion"] = {"x": quaternion[0], "y": quaternion[1], "z": quaternion[2], "w": quaternion[3]}
            # data[d.tag_id] = single_tag_data
            data["camera"][d.tag_id] = single_tag_data
        #check if there are any tags detected
        if len(detections) == 0:
            data = {}
        return img, data

if __name__ == "__main__":
    #search for the server collector service
    zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
    services = ["_camera._udp.local."]
    zeroconf_thread = threading.Thread(target=lambda: ServiceBrowser(zeroconf, services, handlers=[on_service_state_change]))
    zeroconf_thread.start()
    #start the camera
    cap = cv2.VideoCapture(1)
    stream = Stream("my_camera", size=(640, 480), quality=50, fps=30)
    server = MjpegServer("localhost", 8080)
    server.add_stream(stream)
    server.start() 
    camera = Camera(calibration_file_path="calibration_data.json")
    sock = create_udp_socket()
    try:
        while True:
            ret, frame = cap.read()
            img, data = camera.detector_superimpose(frame)
            send_data_over_udp(sock, data, imu_service_ip, imu_service_port)
            stream.set_frame(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        zeroconf.close()
        server.stop()
        sock.close()
        print("Camera service stopped")

