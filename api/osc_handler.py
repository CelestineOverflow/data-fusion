import asyncio
import websockets
import ssl
from pythonosc import udp_client, osc_server, dispatcher, osc_message_builder, osc_bundle_builder
import json

ip = "127.0.0.1"
client_port = 9000

osc_client = udp_client.SimpleUDPClient(ip, client_port)

def osc_build_msg(name, position_or_rotation, args):
    builder = osc_message_builder.OscMessageBuilder(address=f"/tracking/trackers/{name}/{position_or_rotation}")
    builder.add_arg(float(args[0]))
    builder.add_arg(float(args[1]))
    builder.add_arg(float(args[2]))
    return builder.build()

async def handle_message(message):
    try:
        data = json.loads(message)
        print(f"Received message: {data}")
        tracker_name = data.get("tracker")
        position = data.get("position")  # List [x, y, z]
        rotation = data.get("rotation")  # List [x, y, z]

        if position:
            msg = osc_build_msg(tracker_name, "position", position)
            osc_client.send(msg)

        if rotation:
            msg = osc_build_msg(tracker_name, "rotation", rotation)
            osc_client.send(msg)

    except json.JSONDecodeError as e:
        print(f"Invalid JSON message received: {message}")
    except Exception as e:
        print(f"Error handling message: {e}")

async def echo(websocket, path):
    try:
        async for message in websocket:
            await handle_message(message)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected with exception: {e}")

async def main():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(r'D:\data-fusion\viewer\certs\cert.pem', r'D:\data-fusion\viewer\certs\dev.pem')  # Specify the paths to your cert and key files

    async with websockets.serve(echo, "192.168.31.58", 1456, ssl=ssl_context):
        print("Secure WebSocket server started. Listening for clients...")
        await asyncio.Future()  # Run forever

if __name__ == '__main__':
    asyncio.run(main())
