from zeroconf import ServiceInfo, Zeroconf
import socket
import time


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

def register_service(zeroconf, ip, port):
    # create service info for udp listener 
    info = ServiceInfo(type_="_datafusion._udp.local.",
                        name="My awesome service._datafusion._udp.local.",
                            port=port,
                            addresses=[socket.inet_aton(ip)],
                            server="My awesome service.local.")

    zeroconf = Zeroconf()
    zeroconf.register_service(info)

def unregister_service(zeroconf):
    zeroconf.unregister_all_services()
    zeroconf.close()

if __name__ == '__main__':
    try:
        zeroconf = Zeroconf()
        register_service(zeroconf, 1337)
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        unregister_service(zeroconf)
    