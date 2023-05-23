from fastapi import FastAPI
import socket
import threading
import queue
from fastapi.middleware.cors import CORSMiddleware
import json
import random
import time

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
    s.bind((localIP, port))
    while True:
        data, addr = s.recvfrom(bufferSize)
        q.put(data.decode('utf-8'))


@app.get("/")
async def root():
    return {"message": "Hello World"}

t = threading.Thread(target=listen)
t.start()


@app.get("/get")
async def get():
    global q
    # return {"id" : 0,
    #         "accelerometer": {
    #             "x": random.uniform(-1, 1),
    #             "y": random.uniform(-1, 1),
    #             "z": random.uniform(-1, 1)
    #         },
    #         "gyroscope": {
    #             "x": random.uniform(-1, 1),
    #             "y": random.uniform(-1, 1),
    #             "z": random.uniform(-1, 1)
    #         }
    #     }

    if q.empty():
        return {"message": "empty"}
    else:
        try:
            data = json.loads(q.get())
            return data
        except:
            return {"error": "data error from microcontroller"}