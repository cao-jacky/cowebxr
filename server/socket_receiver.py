#!/usr/bin/env python

import asyncio
import pathlib
import ssl
import websockets

import json

import open3d as o3d
import numpy as np

from matplotlib import pyplot as plt

# set array for depth data
depth_2d_array = None

def depth_analyser(client_data):
    depth_data = client_data['depth_data']
        
    data = depth_data['data']
    
    depth_height = depth_data['height']
    depth_width = depth_data['width']
    
    # print(np.shape(data), depth_height, depth_width)
    
    if np.sum(data) != 0: 
        depth_2d_array = np.reshape(data, (depth_height, depth_width))
        depth_2d_array = np.fliplr(np.transpose(depth_2d_array))
        # print(depth_2d_array)
        
        plt.imshow(depth_2d_array, interpolation='nearest')
        # plt.camroll(-90)
        plt.savefig('foo.png')

async def receive(websocket):
    received_data = await websocket.recv()
    try:
        data_json = json.loads(received_data)
        depth_analyser(data_json)
        # print(data_json['depth_data'])
    except:
        pass
    # print(f"<<< {name}")

    # greeting = f"Hello {name}!"
    # await websocket.send(greeting)
    # print(f">>> {greeting}")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
# ssl_context.load_cert_chain(localhost_pem)

cowebxr_pem = pathlib.Path(__file__).with_name("cowebxr.com+3.pem")
cowebxr_key = pathlib.Path(__file__).with_name("cowebxr.com+3-key.pem")

ssl_context.load_cert_chain(cowebxr_pem, keyfile=cowebxr_key, password=None)

async def main():
    async with websockets.serve(receive, "0.0.0.0", 8765, ssl=ssl_context):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())