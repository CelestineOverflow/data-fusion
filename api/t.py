import socket
from time import sleep
from scipy.spatial.transform import Rotation as R
import numpy as np
from zeroconf import IPVersion, ServiceInfo, Zeroconf
import threading
import queue
import json
import asyncio
import websockets
import time
import ssl
import sys

# Global shutdown flag
shutdown_flag = threading.Event()
q = queue.Queue()
clients = set()

# File paths for output
case_type = "imu"
timestamp = time.strftime("%Y%m%d-%H%M%S")
imu_output = f"D:/data-fusion/post-processing/external_input/imu_output_{case_type}_{timestamp}.txt"
latency_output = f"D:/data-fusion/post-processing/static_case_revised/latency_output_{case_type}_{timestamp}.txt"
local_network_ip = socket.gethostbyname(socket.gethostname())
print(f"Local network IP: {local_network_ip}")

def cleanup(file):
    file.close()

imu_to_camera = { 
    "083A8DCC793A": "1",
    "083A8DCCB5BF": "2",
    "083A8DD1B0A6": "3",
    "083A8DCCC2F4": "4",
    "083A8DCCC7B5": "5",
    "58BF25DB53DA": "6",
}

imu_to_ip_port = {
    "083A8DCC793A": {
        "ip": "localhost",
        "port": 4210
    },
    "083A8DCCB5BF": {
        "ip": "localhost",
        "port": 4210
    },
    "083A8DD1B0A6": {
        "ip": "localhost",
        "port": 4210
    },
    "083A8DCCC2F4": {
        "ip": "localhost",
        "port": 4210
    },
    "083A8DCCC7B5": {
        "ip": "localhost",
        "port": 4210   
    },
    "58BF25DB53DA": {
        "ip": "localhost",
        "port": 4210
    }
}

def find_available_port(ip, start_port):
    port = start_port
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.bind((ip, port))
                return port  # The port is available
        except OSError:
            print(f"Port {port} is not available. Trying next port...")
            port += 1  # Increment the port number and try again

def send_orientation_data(ip, port, w, x, y, z):
    # Prepare message
    message = f"{w},{x},{y},{z}"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(message.encode(), (ip, port))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

latest_data_lock = threading.Lock()
latest_data = {}

record_file_latency_path = f"D:/data-fusion/post-processing/static_case_revised/latency_output_{case_type}_{timestamp}.txt"

def udp_server(ip, port, service_name):
    global latest_data
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((ip, port))
        print(f"{service_name} UDP Server listening on {ip}:{port}")
        while not shutdown_flag.is_set():
            try:
                data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
                parsed_data = json.loads(data.decode())
                with latest_data_lock:
                    if "imu" in parsed_data:
                        if "imu" in latest_data:
                            latest_data["imu"].update(parsed_data["imu"])  # Updates only the fields present in the new imu data
                        else:
                            latest_data["imu"] = parsed_data["imu"]  # Initializes imu data if not already present
                    elif "camera" in parsed_data:
                        latest_data["camera"] = parsed_data["camera"]
                    else:
                        print("Unknown data type")
                        pass
                    try:
                        q.put(latest_data, timeout=0.1)  # Timeout to prevent indefinite blocking
                    except queue.Full:
                        print("Queue is full, skipping data")
                    # Handling IMU data
                    if "imu" in parsed_data:
                        for imu_id, imu_data in parsed_data["imu"].items():
                            if imu_id in imu_to_ip_port:
                                imu_to_ip_port[imu_id]["ip"] = addr[0]
                                # print(f"Received IMU data from {imu_id} at {addr[0]}:{addr[1]}")
                    
                    # Handling camera data
                    if "camera" in parsed_data:
                        camera_id = list(parsed_data["camera"].keys())[0]  # Assuming one camera per message for simplification
                        camera_data = parsed_data["camera"][camera_id]
                        for imu_id, cam_id in imu_to_camera.items():
                            if cam_id == camera_id:
                                imu_details = imu_to_ip_port[imu_id]
                                quat = camera_data["quaternion"]
                                
                                quat_test2 = R.from_quat([quat["x"], quat["y"], quat["z"], quat["w"]])

                                # Create a quaternion from an axis-angle representation
                                axis = [1, 0, 0]
                                angle = np.pi / 2
                                rotation_quat = R.from_rotvec(np.multiply(axis, angle))

                                # Premultiply the original quaternion by the new quaternion
                                resulting_quat = rotation_quat * quat_test2
                            
                                # Now use the rotated quaternion in your function call
                                print(f"Sending orientation data to IMU {imu_details}")
                                
                                send_orientation_data(
                                    imu_details["ip"], 
                                    imu_details["port"], 
                                    resulting_quat.as_quat()[3],
                                    resulting_quat.as_quat()[0],
                                    resulting_quat.as_quat()[1],
                                    resulting_quat.as_quat()[2]
                                )
            except json.JSONDecodeError:
                print(f"Error parsing data: {data}")
                continue
            except socket.timeout:
                continue  # Go back to the start of the loop if the socket times out
            except OSError:
                break  # Exit the loop if the socket is closed

def register_service(ip, port, name, type_):
    desc = {'description': f'{name} Service'}
    service_name = f"{name}.{type_}"
    info = ServiceInfo(
        type_,
        service_name,
        addresses=[socket.inet_aton(ip)],
        port=port,
        properties=desc,
        server=f"{name}.local.",
    )

    zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
    try:
        print(f"Registering {name} service, press Ctrl-C to exit...")
        zeroconf.register_service(info)
        while not shutdown_flag.is_set():
            sleep(0.1)
    finally:
        print(f"Unregistering {name} service...")
        zeroconf.unregister_service(info)
        zeroconf.close()

async def register_client(websocket):
    print(f"Client {websocket.remote_address} connected")
    clients.add(websocket)

async def unregister_client(websocket):
    print(f"Client {websocket.remote_address} disconnected")
    clients.remove(websocket)

async def send_to_clients(message):
    if clients:
        tasks = []
        for client in clients.copy():
            try:
                tasks.append(client.send(message))
            except websockets.exceptions.ConnectionClosed:
                print(f"Client {client.remote_address} disconnected")
                clients.remove(client)
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

async def handle_queue():
    while True:
        if not q.empty():
            while not q.empty():
                data = q.get()
            await send_to_clients(json.dumps(data))
        await asyncio.sleep(0.01)  # Prevents the loop from hogging the CPU

async def websocket_server(websocket, path):
    print(f"Client {websocket.remote_address} connected")
    await register_client(websocket)
    try:
        await websocket.wait_closed()
    finally:
        await unregister_client(websocket)

async def main():
    # Set up WebSocket server
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(r'D:\data-fusion\front_end\cert.crt', r'D:\data-fusion\front_end\cert.key')
    global local_network_ip
    start_server = websockets.serve(websocket_server, local_network_ip, 1456, ssl=ssl_context)

    # Run the server and handle the queue concurrently
    await asyncio.gather(
        start_server,
        handle_queue(),
    )

def t():
    asyncio.run(main())

def shutdown():
    print("Shutting down...")
    shutdown_flag.set()  # Signal all threads to shut down
    for thread in threads:
        thread.join()
    sys.exit(0)

if __name__ == '__main__':
    try:
        start_time = time.time()
        print(f"Local network IP: {local_network_ip}")
        
        #write to file 
        file_path = '../front_end/src/stores/websocket.ts'
        data = None
        with open(file_path, 'r') as file:
            print(f"Updating websocket.js with local network IP: {local_network_ip}")
            #read a list of lines into data
            data = file.readlines()
            for i in range(len(data)):
                if 'let socket = new WebSocket("' in data[i]:
                    data[i] = f'    let socket = new WebSocket("wss://{local_network_ip}:1456");\n'
        # and write everything back
        with open(file_path, 'w') as file:
            file.writelines(data)
            print(f"Updated websocket.js with local network IP: {local_network_ip}")
        # Check ports for availability
        imu_udp_listener_port = find_available_port(local_network_ip, 6969)
        camera_udp_listener_port = find_available_port(local_network_ip, 4242)

        threads = [
            threading.Thread(target=udp_server, args=(local_network_ip, imu_udp_listener_port, "IMU")),
            threading.Thread(target=register_service, args=(local_network_ip, imu_udp_listener_port, "IMUService", "_imu._udp.local.")),
            threading.Thread(target=udp_server, args=(local_network_ip, camera_udp_listener_port, "Camera")),
            threading.Thread(target=register_service, args=(local_network_ip, camera_udp_listener_port, "CameraService", "_camera._udp.local.")),
            threading.Thread(target=t)
        ]
        
        # Start the queue listener in a separate thread
        for thread in threads:
            thread.start()

        while not shutdown_flag.is_set():
            time.sleep(1)  # Main thread can sleep or perform other tasks, checking periodically if it's time to shut down
    except Exception as e:
        print(f"An error occurred: {e}")
