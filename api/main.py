from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response
import io
from fastapi.responses import StreamingResponse
import socket
import threading
import queue
from fastapi.middleware.cors import CORSMiddleware
import json
import random
import time
import asyncio
import utils.mdns_registered as mdns_registered
from zeroconf import ServiceInfo, Zeroconf
from pythonosc.udp_client import SimpleUDPClient
import socket
import camera as cmr
import traceback



#get ip in local network
local_network_ip = socket.gethostbyname(socket.gethostname())
print(local_network_ip)
#setup osc client
client = SimpleUDPClient(local_network_ip, 9000)


local_network_ip=mdns_registered.get_local_ip()
port = 1337


bufferSize = 1024
q = queue.Queue(10)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


osc_addresses = {
    "head": {
        "position": "/tracking/trackers/head/position",
        "rotation": "/tracking/trackers/head/rotation"
    },
    "tracker1": {
        "position": "/tracking/trackers/1/position",
        "rotation": "/tracking/trackers/1/rotation"
    },
    "tracker2": {
        "position": "/tracking/trackers/2/position",
        "rotation": "/tracking/trackers/2/rotation"
    },
    "tracker3": {
        "position": "/tracking/trackers/3/position",
        "rotation": "/tracking/trackers/3/rotation"
    },
    "tracker4": {
        "position": "/tracking/trackers/4/position",
        "rotation": "/tracking/trackers/4/rotation"
    },
    "tracker5": {
        "position": "/tracking/trackers/5/position",
        "rotation": "/tracking/trackers/5/rotation"
    },
    "tracker6": {
        "position": "/tracking/trackers/6/position",
        "rotation": "/tracking/trackers/6/rotation"
    },
    "tracker7": {
        "position": "/tracking/trackers/7/position",
        "rotation": "/tracking/trackers/7/rotation"
    },
    "tracker8": {
        "position": "/tracking/trackers/8/position",
        "rotation": "/tracking/trackers/8/rotation"
    }
}

class Vector3():
    
    def __init__(self, x: float, y: float, z: float):
        """
        Creates a Vector3 instance.
        
        Parameters:
        x (float): X coordinate.
        y (float): Y coordinate.
        z (float): Z coordinate.
        """
        self.x = x
        self.y = y
        self.z = z
        
    def to_vector(self) -> tuple:
        """
        Returns a tuple of the vector coordinates.
        """
        return (self.x, self.y, self.z)
    

tracker_initial_pose = {
    "head": {
        "position": Vector3 (0.0, -0.1, -0.1),
        "rotation": Vector3 (0.0, 0.0, 0.0)
    },
    "tracker1": {
        "position": Vector3 (0.007038268726319075, -0.4179477095603943, -0.13543081283569336),
        "rotation": Vector3 (6.355330944061279, 0.14127297699451447, 1.275995135307312)
    }
    
}



def register_service(ip, port):
    z = Zeroconf()
    mdns_registered.register_service(z, local_network_ip, port)
    print("UDP server IP address: " + local_network_ip + ":" + str(port))
offset_sent = True

def send_orientation_data(ip, port, pitch, roll, yaw):
    message = f"{pitch},{roll},{yaw}"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(message.encode(), (ip, port))
        print(f"Sent: {message}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()


def listen():
    global local_network_ip
    global port
    global bufferSize
    global q
    global offset_sent
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.1)
    s.bind((local_network_ip, port))
    start_t = time.time()
    print("UDP server up and listening")
    d = {"id":0,"accelerometer":{"x":0,"y":-0.08,"z":1.04},"gyroscope":{"x":0,"y":-0.12,"z":0.1}}
    while True:
        try:
            data, addr = s.recvfrom(bufferSize)
            data = data.decode('utf-8')
            # print(data)
            try:
                parsed_data = json.loads(data)
            
                x = parsed_data["orientation"]["pitch"]
                y = parsed_data["orientation"]["roll"]
                z = parsed_data["orientation"]["yaw"]
                #convert to float and degrees
                x = float(x) * 180 / 3.141592653589793
                y = float(y) * 180 / 3.141592653589793
                z = float(z) * 180 / 3.141592653589793
                
                # client.send_message(osc_addresses["head"]["position"], tracker_initial_pose["head"]["position"].to_vector())
                # client.send_message(osc_addresses["head"]["rotation"], tracker_initial_pose["head"]["rotation"].to_vector())
                client.send_message(osc_addresses["tracker1"]["position"], tracker_initial_pose["tracker1"]["position"].to_vector())
                client.send_message(osc_addresses["tracker1"]["rotation"], (x, y, z))
                q.put(data)
                if not offset_sent:
                    print("sending offset")
                    #send rotation only from camera to mcu
                    # s.sendto(json.dumps(latest_camera_data).encode('utf-8'), (addr[0], 4210))
                    rotation = latest_camera_data["rotation"].copy()
                    #convert to float and degrees
                    rotation["x"] = float(rotation["x"]) * 180 / 3.141592653589793
                    rotation["y"] = float(rotation["y"]) * 180 / 3.141592653589793
                    rotation["z"] = float(rotation["z"]) * 180 / 3.141592653589793
                    send_orientation_data(addr[0], 4210, rotation["x"], rotation["y"], rotation["z"])
                    offset_sent = True
            except Exception as e:
                print(e)
                print("error parsing data")
                continue
            
        except socket.timeout:
            pass


@app.get("/")
async def root():
    return {"message": "Hello there you beautiful person!, go to /docs for the api documentation"}

t0 = threading.Thread(target=register_service, args=(local_network_ip, port))
t0.start()
time.sleep(5)
t = threading.Thread(target=listen)
t.start()


@app.get("/get")
async def get():
    global q

    if q.empty():
        return {"message": "empty"}
    else:
        try:
            data = json.loads(q.get())
            return data
        except Exception as e:
            return {"error": "data error from microcontroller e: " + str(e)}

camera = cmr.Camera(calibration_file_path="calibration_data.json", camera_id=1)

@app.get("/setCamera/{id}")
def set_camera(id: int):
    camera.set_camera(id)
@app.get("/video")
def video_endpoint():
    return camera.video_endpoint()

latest_camera_data = {"id":19,"position":{"x":0.31799993733185844,"y":0.0719889898174673,"z":2.9135152263236006},"rotation":{"x":-0.13036970754792743,"y":0.30010247141273116,"z":0.7551000454510922}}
latest_mcu_data = {}
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global q
    global latest_camera_data
    global latest_mcu_data
    global offset_sent
    await websocket.accept()
    while True:
        if q.empty():
            await asyncio.sleep(0.01)
        else:
            try:
                mcu_data = json.loads(q.get())
                #if mcu isnt empty
                if mcu_data:
                    latest_mcu_data = mcu_data
                camera_data = camera.getData()
                #if camera isnt empty
                if camera_data is not None:
                    latest_camera_data = camera_data
                    offset_sent = False
                #if both arent empty
                await websocket.send_json({"camera": latest_camera_data, "mcu": latest_mcu_data})
                
            except Exception as e:
                traceback.print_exc()

            
            
            



