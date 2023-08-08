#!/usr/bin/env python

import asyncio
import pathlib
import ssl
import websockets

async def hello(websocket):
    name = await websocket.recv()
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f">>> {greeting}")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
# ssl_context.load_cert_chain(localhost_pem)

cowebxr_pem = pathlib.Path(__file__).with_name("cowebxr.com+3.pem")
cowebxr_key = pathlib.Path(__file__).with_name("cowebxr.com+3-key.pem")

ssl_context.load_cert_chain(cowebxr_pem, keyfile=cowebxr_key, password=None)

async def main():
    async with websockets.serve(hello, "0.0.0.0", 8765, ssl=ssl_context):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())