import asyncio
import websockets
import ssl

async def hello():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    uri = "wss://192.168.31.58:1456/"
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        await websocket.send("Hello server!")
        response = await websocket.recv()
        print(response)

asyncio.run(hello())
