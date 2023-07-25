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

def register_service(ip, port):
    z = Zeroconf()
    mdns_registered.register_service(z, local_network_ip, port)
    print("UDP server IP address: " + local_network_ip + ":" + str(port))

def listen():
    global local_network_ip
    global port
    global bufferSize
    global q
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
            data = json.loads(data)
            print(data)
            if "accelerometer" in data and "gyroscope" in data: #data from imu
                d["type"] = "accelerometer-gyroscope-vector"
                d["id"] = data["id"]
                d["accelerometer"]["x"] = data["accelerometer"]["x"]
                d["accelerometer"]["y"] = data["accelerometer"]["y"]
                d["accelerometer"]["z"] = data["accelerometer"]["z"] 
                d["gyroscope"]["x"] = data["gyroscope"]["x"]
                d["gyroscope"]["y"] = data["gyroscope"]["y"]
                d["gyroscope"]["z"] = data["gyroscope"]["z"]
                q.put(json.dumps(d))
            else:
                #just send back the data
                q.put(json.dumps(data))
        except socket.timeout:
            pass


@app.get("/")
async def root():
    return {"message": "Hello there you beautiful person!"}

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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # data = await websocket.receive_text()
        # # await websocket.send_text(f"Message text was: {data}")
        # #send json response
        # await websocket.send_text(json.dumps({"message": "Hello WebSocket"}))
        if q.empty():
            #asynchronous sleep
            await asyncio.sleep(0.01)
        else:
            try:
                data = json.loads(q.get())
                await websocket.send_text(json.dumps(data))
            except:
                await websocket.send_text(json.dumps({"error": "data error from microcontroller"}))
                continue