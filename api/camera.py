import cv2
import pupil_apriltags as apriltag
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import json
import threading
import socket

data = {"id":1,"position":{"x":0,"y":-0.08,"z":1.04},"rotation":{"x":0,"y":-0.12,"z":0.1}}

import utils.mdns_registered as mdns
local_network_ip = mdns.get_local_ip()
port = 1337

def send_data(data):
    data = json.dumps(data)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    global local_network_ip
    s.sendto(data.encode('utf-8'), (local_network_ip, port))
    s.close()

def load_calibration_file(calibration_file_path):
    #reconstruct the camera matrix and distortion coefficients
    with open(calibration_file_path, 'r') as infile:
        reconstruction = json.load(infile)
        mtx = np.array(reconstruction['mtx'])
        mtx = [mtx[0,0], mtx[1,1], mtx[0,2], mtx[1,2]]
        dist = np.array(reconstruction['dist'])
        return mtx, dist

def detector_superimpose(img, detector, mtx, dist, tag_size=0.16):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(gray, estimate_tag_pose= True, camera_params=(mtx), tag_size=tag_size)
    for d in detections:
        pose_data = d.pose_R, d.pose_t
        rvec, tvec = pose_data[0], pose_data[1]
        quat = sp.spatial.transform.Rotation.from_matrix(rvec).as_quat()
        euler = sp.spatial.transform.Rotation.from_matrix(rvec).as_euler('xyz', degrees=False)
        x, y, z = euler[0], euler[1], euler[2]
        tx, ty, tz = tvec[0][0], tvec[1][0], tvec[2][0]
        cv2.circle(img, (int(d.center[0]), int(d.center[1])), 5, (0, 0, 255), -1)
        cv2.putText(img, str(d.tag_id), (int(d.center[0]), int(d.center[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        #draw angle and position of tag
        cv2.putText(img, "x: " + str(round(x, 2)), (int(d.center[0]), int(d.center[1]) + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, "y: " + str(round(y, 2)), (int(d.center[0]), int(d.center[1]) + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, "z: " + str(round(z, 2)), (int(d.center[0]), int(d.center[1]) + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # print("tvex: ", tvec)
        # #shape:  (3, 1)
        # print("shape: ", tvec.shape)
        cv2.putText(img, "t x: " + str(round(tvec[0][0], 2)), (int(d.center[0]), int(d.center[1]) + 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, "t y: " + str(round(tvec[1][0], 2)), (int(d.center[0]), int(d.center[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, "t z: " + str(round(tvec[2][0], 2)), (int(d.center[0]), int(d.center[1]) + 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        data["id"] = d.tag_id
        data["position"]["x"] = tvec[0][0]
        data["position"]["y"] = tvec[1][0]
        data["position"]["z"] = tvec[2][0]
        data["rotation"]["x"] = x
        data["rotation"]["y"] = y
        data["rotation"]["z"] = z
        #send data to udp server
        send_data(data)
    return img
        
def live_feed(camera_id, mtx, dist):
    cap = cv2.VideoCapture(camera_id)
    detector = apriltag.Detector(families='tag36h11', nthreads=1, quad_decimate=1.0, quad_sigma=0.0, refine_edges=1, decode_sharpening=0.25, debug=0)
    while True:
        ret, frame = cap.read()
        if ret:
            frame = detector_superimpose(frame, detector, mtx, dist)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("error reading frame")
            break
    cap.release()
    cv2.destroyAllWindows() 

if __name__ == "__main__":
    #do unthreaded version
    mtx, dist = load_calibration_file(r'calibration_data.json')
    live_feed(2, mtx, dist)
    