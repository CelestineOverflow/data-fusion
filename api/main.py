from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import socket
import threading
import queue
from fastapi.middleware.cors import CORSMiddleware
import json
import random
import time
import asyncio

# allow all bulshit origin idgaf


localIP = '192.168.31.242'
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


def listen():
    global localIP
    global port
    global bufferSize
    global q
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.1)
    s.bind((localIP, port))
    start_t = time.time()
    print("UDP server up and listening")
    d = {"id":0,"position":{"x":0,"y":-0.08,"z":1.04},"rotation":{"x":0,"y":-0.12,"z":0.1}}
    while True:
        try:
            delta_t = time.time() - start_t
            data, addr = s.recvfrom(bufferSize)
            data = data.decode('utf-8')
            data = json.loads(data)
            d["id"] = data["id"]
            d["position"]["x"] = data["accelerometer"]["x"]
            d["position"]["y"] = data["accelerometer"]["y"]
            d["position"]["z"] = data["accelerometer"]["z"] 
            d["rotation"]["x"] = data["gyroscope"]["x"] * delta_t
            d["rotation"]["y"] = data["gyroscope"]["y"] * delta_t
            d["rotation"]["z"] = data["gyroscope"]["z"] * delta_t
            q.put(json.dumps(d))
            start_t = time.time()
        except socket.timeout:
            pass


@app.get("/")
async def root():
    return {"message": "Hello World"}

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
        except:
            return {"error": "data error from microcontroller"}
        
        
#websockets
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