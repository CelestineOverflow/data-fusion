# import cv2
# import pupil_apriltags as apriltag
# import numpy as np
# import scipy as sp
# import json
# import cv2
# import pupil_apriltags as apriltag
# import numpy as np
# import scipy as sp
# import json
# from fastapi.responses import StreamingResponse



# data = {"id":1,"position":{"x":0,"y":-0.08,"z":1.04},"rotation":{"x":0,"y":-0.12,"z":0.1}}


# asDegree = False

# def load_calibration_file(calibration_file_path):
#     #reconstruct the camera matrix and distortion coefficients
#     with open(calibration_file_path, 'r') as infile:
#         reconstruction = json.load(infile)
#         mtx = np.array(reconstruction['mtx'])
#         mtx = [mtx[0,0], mtx[1,1], mtx[0,2], mtx[1,2]]
#         dist = np.array(reconstruction['dist'])
#         return mtx, dist

# def detector_superimpose(img, detector, mtx, dist, tag_size=0.16):
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     detections = detector.detect(gray, estimate_tag_pose= True, camera_params=(mtx), tag_size=tag_size)
#     for d in detections:
#         pose_data = d.pose_R, d.pose_t
#         rvec, tvec = pose_data[0], pose_data[1]
#         sp.spatial.transform.Rotation.from_matrix(rvec).as_quat()
#         rotation = sp.spatial.transform.Rotation.from_matrix(rvec).as_euler('xyz', degrees=asDegree)
#         x, y, z = rotation[0], rotation[1], rotation[2]
#         cv2.circle(img, (int(d.center[0]), int(d.center[1])), 5, (0, 0, 255), -1)
#         cv2.putText(img, str(d.tag_id), (int(d.center[0]), int(d.center[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#         #draw angle and position of tag
#         cv2.putText(img, "x: " + str(round(x, 2)), (int(d.center[0]), int(d.center[1]) + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#         cv2.putText(img, "y: " + str(round(y, 2)), (int(d.center[0]), int(d.center[1]) + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#         cv2.putText(img, "z: " + str(round(z, 2)), (int(d.center[0]), int(d.center[1]) + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#         cv2.putText(img, "t x: " + str(round(tvec[0][0], 2)), (int(d.center[0]), int(d.center[1]) + 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#         cv2.putText(img, "t y: " + str(round(tvec[1][0], 2)), (int(d.center[0]), int(d.center[1]) + 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#         cv2.putText(img, "t z: " + str(round(tvec[2][0], 2)), (int(d.center[0]), int(d.center[1]) + 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#         data["id"] = d.tag_id
#         data["position"]["x"] = tvec[0][0]
#         data["position"]["y"] = tvec[1][0]
#         data["position"]["z"] = tvec[2][0]
#         data["rotation"]["x"] = x
#         data["rotation"]["y"] = y
#         data["rotation"]["z"] = z
#     return img, data
        
# def live_feed(camera_id, mtx, dist):
#     cap = cv2.VideoCapture(camera_id)
#     detector = apriltag.Detector(families='tag36h11', nthreads=1, quad_decimate=1.0, quad_sigma=0.0, refine_edges=1, decode_sharpening=0.25, debug=0)
#     while True:
#         ret, frame = cap.read()
#         if ret:
#             frame, data = detector_superimpose(frame, detector, mtx, dist)
#             cv2.imshow('frame', frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#         else:
#             print("error reading frame")
#             break
#     cap.release()
#     cv2.destroyAllWindows() 

# mtx, dist = load_calibration_file(r"D:\data-fusion\api\calibration_data.json")
# detector = apriltag.Detector(families='tag36h11', nthreads=1, quad_decimate=1.0, quad_sigma=0.0, refine_edges=1, decode_sharpening=0.25, debug=0)

# def generate_frames():
#     while True:
#         success, frame = capture.read()  # read a frame from the camera
#         if not success:
#             break
#         else:
#             img, data = detector_superimpose(frame, detector, mtx, dist)
#             img = cv2.imencode('.jpg', img)[1].tobytes()
#             yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
# def set_camera(id: int):
#     global capture
#     capture = cv2.VideoCapture(id)
#     return {"message": "camera set to id: " + str(id)}


# def video_endpoint():
#     if capture is None:
#         return {"message": "camera not set"}
#     if not capture.isOpened():
#         return {"message": "camera not opened"}
#     return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace;boundary=frame")



import cv2
import pupil_apriltags as apriltag
import numpy as np
import scipy as sp
import json
import queue
from fastapi.responses import StreamingResponse

data = {"id":1,"position":{"x":0,"y":-0.08,"z":1.04},"rotation":{"x":0,"y":-0.12,"z":0.1}, "quaternion": {"x": 0, "y": 0, "z": 0, "w": 0}}
asDegree = False

class Camera:
    def __init__(self, calibration_file_path, camera_id=None):
        self.data = {"id": 1, "position": {"x": 0, "y": -0.08, "z": 1.04}, "rotation": {"x": 0, "y": -0.12, "z": 0.1}}
        self.asDegree = False
        self.mtx, self.dist = self.load_calibration_file(calibration_file_path)
        self.detector = apriltag.Detector(families='tag36h11', nthreads=1, quad_decimate=1.0, quad_sigma=0.0, refine_edges=1, decode_sharpening=0.25, debug=0)
        self.capture = None
        self.q = queue.Queue()
        if camera_id is not None:
            self.set_camera(camera_id)

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
        for d in detections:
            pose_data = d.pose_R, d.pose_t
            rvec, tvec = pose_data[0], pose_data[1]
            quaternion = sp.spatial.transform.Rotation.from_matrix(rvec).as_quat()
            
            
            rotation = sp.spatial.transform.Rotation.from_matrix(rvec).as_euler('xyz', degrees=asDegree)
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
            data["id"] = d.tag_id
            data["position"]["x"] = tvec[0][0]
            data["position"]["y"] = tvec[1][0]
            data["position"]["z"] = tvec[2][0]
            data["quaternion"] = {"x": quaternion[0], "y": quaternion[1], "z": quaternion[2], "w": quaternion[3]}
            data["rotation"]["x"] = x
            data["rotation"]["y"] = y
            data["rotation"]["z"] = z
            
            # rotate by pi/2 quaternion
            new_quaternion = np.array([0, 0, 1, 0])
            data["quaternion"]["x"] = quaternion[0] * new_quaternion[0] - quaternion[1] * new_quaternion[1] - quaternion[2] * new_quaternion[2] - quaternion[3] * new_quaternion[3]
            data["quaternion"]["y"] = quaternion[0] * new_quaternion[1] + quaternion[1] * new_quaternion[0] + quaternion[2] * new_quaternion[3] - quaternion[3] * new_quaternion[2]
            data["quaternion"]["z"] = quaternion[0] * new_quaternion[2] - quaternion[1] * new_quaternion[3] + quaternion[2] * new_quaternion[0] + quaternion[3] * new_quaternion[1]
            data["quaternion"]["w"] = quaternion[0] * new_quaternion[3] + quaternion[1] * new_quaternion[2] - quaternion[2] * new_quaternion[1] + quaternion[3] * new_quaternion[0]
            
            
            
        if len(detections) == 0:
            return img, None
        return img, data
        

    def set_camera(self, camera_id):
        self.capture = cv2.VideoCapture(camera_id)

    def generate_frames(self):
        while True:
            success, frame = self.capture.read()
            if not success:
                break
            else:
                img, data = self.detector_superimpose(frame)
                self.q.put(data)
                img = cv2.imencode('.jpg', img)[1].tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

    def getData(self):
        "iterate through the queue and return the last element"
        data = None
        while not self.q.empty():
            data = self.q.get()
        return data
    
    def video_endpoint(self):
        if self.capture is None:
            return {"message": "camera not set"}
        if not self.capture.isOpened():
            return {"message": "camera not opened"}
        return StreamingResponse(self.generate_frames(), media_type="multipart/x-mixed-replace;boundary=frame")