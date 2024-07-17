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
import json
from queue import Queue
import time
import threading
# Global shutdown flag
shutdown_flag = threading.Event()
q = queue.Queue(10)
clients = set()
import atexit
import sys
import time
import signal
import ssl
# File paths for output
case_type = "static-camera"
timestamp = time.strftime("%Y%m%d-%H%M%S")
imu_output = f"D:/data-fusion/post-processing/external_input/imu_output_{case_type}_{timestamp}.txt"
latency_output = f"D:/data-fusion/post-processing/static_case_revised/latency_output_{case_type}_{timestamp}.txt"
local_network_ip = socket.gethostbyname(socket.gethostname())
print(f"Local network IP: {local_network_ip}")

def cleanup(file):
    file.close
#routing 
routing_table = {
    "bodyPart": {
        "chest": {
            "imu": {
                "ip": "localhost",
                "port": 4210,
                "id": "083A8DCCC7B5"
            },
            "camera": {
                "id": "2",}
        },
        "leftUpperArm": {
            "imu": {
                "ip": "localhost",
                "port": 4210,
                "id": "083A8DCCC2F4"
            },
            "camera": {
                "id": "1",}
        },
        "rigthUpperArm": {
            "imu": {
                "ip": "localhost",
                "port": 4210,
                "id": "98CDAC1D78E6"
            },
            "camera": {
                "id": "3",}
        },
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




def imuOutput2File(data):
    file = open(imu_output, 'a')
    timestamp = time.perf_counter()
    file.write(str(timestamp) + '   ' +  json.dumps(data)+ '\n')
    file.flush()
    file.close()
    
def latencyOutput2File(data):
    file = open(latency_output, 'a')
    timestamp = time.perf_counter()
    file.write(str(timestamp) + '   ' + data + '\n')
    file.flush()
    file.close()

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

latest_data = {}

def udp_server(ip, port, service_name):
    global latest_data
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((ip, port))
        print(f"{service_name} UDP Server listening on {ip}:{port}")
        while not shutdown_flag.is_set():
            try:
                data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
                parsed_data = json.loads(data.decode())
                
                if "imu" in parsed_data:
                    if "imu" in latest_data:
                        latest_data["imu"].update(parsed_data["imu"])  # Updates only the fields present in the new imu data
                    else:
                        latest_data["imu"] = parsed_data["imu"]  # Initializes imu data if not already present
                    # latencyOutput2File('imu')
                elif "camera" in parsed_data:
                    latest_data["camera"] = parsed_data["camera"]
                    # latencyOutput2File('camera')
                else:
                    print("Unknown data type")
                    pass
                q.put(latest_data)
                # # Handling IMU data
                if "imu" in parsed_data:
                    # print("imu")
                    for imu_id, imu_data in parsed_data["imu"].items():
                        for part, details in routing_table["bodyPart"].items():
                            if details["imu"]["id"] == imu_id:
                                details["imu"]["ip"] = addr[0]
                                # print(f"Received IMU data from {imu_id} at {addr[0]}:{addr[1]}")
                                
                
                # # Handling camera data
                if "camera" in parsed_data:
                    # print("camera")
                    # Assuming camera data includes a direct mapping to an IMU ID or another identifier that can be used to find the corresponding IMU
                    camera_id = list(parsed_data["camera"].keys())[0]  # Assuming one camera per message for simplification
                    camera_data = parsed_data["camera"][camera_id]
                    for part, details in routing_table["bodyPart"].items():
                        if details["camera"]["id"] == camera_id:
                            imu_details = details["imu"]
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
                            #send_orientation_data(imu_details["ip"], imu_details["port"], quat["w"], quat["x"], quat["y"], quat["z"])
                            # print(f"Sent camera data from {camera_id} to IMU {details['imu']['id']}")
                            
                # imuOutput2File(latest_data)
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
    if clients:  # Check if there are any clients connected
        # print(f"Sending message to {len(clients)} clients")
        # Wrap each coroutine in a task using asyncio.create_task()
        tasks = [asyncio.create_task(client.send(message)) for client in clients]
        await asyncio.wait(tasks)


async def handle_queue():
    while True:
        if not q.empty():
            while not q.empty():
                data = q.get()
            await send_to_clients(json.dumps(data))
        await asyncio.sleep(0.01)  # Prevents the loop from hogging the CPU

async def websocket_server(websocket, path):
    await register_client(websocket)
    try:
        await websocket.wait_closed()
    finally:
        await unregister_client(websocket)

async def main():
    # Set up WebSocket server
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(r'..\front_end\cert.pem', r'D:\data-fusion\front_end\dev.pem')  # Specify the paths to your cert and key files
    global local_network_ip
    start_server = websockets.serve(websocket_server, local_network_ip, 1456, ssl=ssl_context)
    # start_server = websockets.serve(websocket_server, "localhost", 6789)

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
    # Clean up resources, close sockets, files, etc.
    # You might need to signal your threads or async loops to check the shutdown_flag and exit cleanly
    sys.exit(0)  # Forcefully exits the script. Use if necessary, otherwise let threads exit gracefully.



if __name__ == '__main__':
    try:
        # shutdown_timer = threading.Timer(1*60, shutdown)
        # shutdown_timer.start()  # Start the timer
        start_time = time.time()
        print(f"Local network IP: {local_network_ip}")
        # Check ports for availability
        # Global UDP listener ports
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
            time.sleep(1)  # Main fthread can sleep or perform other tasks, checking periodically if it's time to shut down
    except Exception as e:
        print(f"An error occurred: {e}")
    
    #     shutdown_flag.set()
    #     for thread in threads:
    #         thread.join()
