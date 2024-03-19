import socket
from time import sleep
from zeroconf import IPVersion, ServiceInfo, Zeroconf
import threading
import queue
import json
# Global shutdown flag
shutdown_flag = threading.Event()
q = queue.Queue(10)

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
                "id": "17",}
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


def send_orientation_data(ip, port, w, x, y, z):
    message = f"{w},{x},{y},{z}"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(message.encode(), (ip, port))
        # print(f"Sent: {message}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()


def udp_server(ip, port, service_name):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((ip, port))
        print(f"{service_name} UDP Server listening on {ip}:{port}")

        while not shutdown_flag.is_set():
            try:
                data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
                parsed_data = json.loads(data.decode())
                # print(f"Received data from {addr}: {parsed_data}")
                # Handling IMU data to dynamically update its IP based on ID
                if "imu" in parsed_data:
                    for imu_id, imu_data in parsed_data["imu"].items():
                        for part, details in routing_table["bodyPart"].items():
                            if details["imu"]["id"] == imu_id:
                                # Update IMU's IP and port dynamically
                                details["imu"]["ip"] = addr[0]
                                # print(f"Updated IP for IMU {imu_id} to {addr[0]}")
                
                # Handling camera data
                if "camera" in parsed_data:
                    # Assuming camera data includes a direct mapping to an IMU ID or another identifier that can be used to find the corresponding IMU
                    camera_id = list(parsed_data["camera"].keys())[0]  # Assuming one camera per message for simplification
                    camera_data = parsed_data["camera"][camera_id]
                    # Example on how you might need to link a camera to an IMU, assuming a direct or indirect linkage exists
                    # For demonstration, using the camera ID to directly get the corresponding IMU ID might require a mapping or a direct relation like below
                    for part, details in routing_table["bodyPart"].items():
                        if details["camera"]["id"] == camera_id:
                            imu_details = details["imu"]
                            # Assuming quaternion data is structured correctly in the camera data
                            quat = camera_data["quaternion"]
                            send_orientation_data(imu_details["ip"], imu_details["port"], quat["w"], quat["x"], quat["y"], quat["z"])
                            # print(f"Sent camera data from {camera_id} to IMU {details['imu']['id']}")
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

if __name__ == '__main__':
    try:
        local_network_ip = socket.gethostbyname(socket.gethostname())
        # Check ports for availability
        # Global UDP listener ports
        imu_udp_listener_port = find_available_port(local_network_ip, 6969)
        camera_udp_listener_port = find_available_port(local_network_ip, 4242)

        threads = [
            threading.Thread(target=udp_server, args=(local_network_ip, imu_udp_listener_port, "IMU")),
            threading.Thread(target=register_service, args=(local_network_ip, imu_udp_listener_port, "IMUService", "_imu._udp.local.")),
            threading.Thread(target=udp_server, args=(local_network_ip, camera_udp_listener_port, "Camera")),
            threading.Thread(target=register_service, args=(local_network_ip, camera_udp_listener_port, "CameraService", "_camera._udp.local."))
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
    except:
        shutdown_flag.set()
        for thread in threads:
            thread.join()
