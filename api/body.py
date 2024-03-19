
from time import sleep
from typing import cast

from zeroconf import (
    IPVersion,
    ServiceBrowser,
    ServiceStateChange,
    Zeroconf,
    ZeroconfServiceTypes,
)

imu_service_ip = ""
imu_service_port = 5000

def on_service_state_change(
    zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange
) -> None:
    # print(f"Service {name} of type {service_type} state changed: {state_change}")

    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        print("Info from zeroconf.get_service_info: %r" % (info))
        imu_service_ip = info.parsed_addresses()[0]
        imu_service_port = info.port
        print(f"IMU Service IP: {imu_service_ip}, Port: {imu_service_port}")


if __name__ == '__main__':
    zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
    services = ["_camera._udp.local."]
    print("\nBrowsing %d service(s), press Ctrl-C to exit...\n" % len(services))
    browser = ServiceBrowser(zeroconf, services, handlers=[on_service_state_change])

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()