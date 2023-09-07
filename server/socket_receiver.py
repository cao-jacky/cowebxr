#!/usr/bin/env python

import asyncio
import pathlib
import ssl
import websockets

import json

import open3d as o3d
import numpy as np

from matplotlib import pyplot as plt

from PIL import Image
import io
import glob

# set array for depth data
depth_2d_array = None

paths = {
    'rgb': 'client_data/image',
    'depth': 'client_data/depth'
}
    
def rgb_depth_analyser(client_data):
    depth_head = client_data['depth_data']
    rgb_head = client_data['rgb_data']
    
    depth_data = depth_head['data']
    rgb_data = rgb_head['data']
    
    depth_scaling = depth_head['scale']
        
    depth_height = depth_head['height']
    depth_width = depth_head['width']
    
    # print(np.shape(data), depth_height, depth_width)
        
    # fig, axs = plt.subplots(1, 2, figsize=(10, 7))

    if np.sum(depth_data) != 0: 
        depth_2d_array = np.reshape(depth_data, (depth_height, depth_width))
        depth_2d_array = np.fliplr(np.transpose(depth_2d_array)) 
        depth_2d_array = depth_2d_array * depth_head['scale']
        print(np.min(depth_2d_array), np.max(depth_2d_array))
        
        fig, axs = plt.subplots(1, 1, figsize=(10, 7))
        axs.imshow(depth_2d_array, interpolation='nearest')
        axs.axis('off')
        
        depth_folder = paths['depth']
        curr_depth_files = len(glob.glob(f'{depth_folder}/*.png'))
        plt.savefig(f'{depth_folder}/{curr_depth_files+1}.png')
        plt.close()

        image_bytes = bytes(rgb_data)
        image_stream = io.BytesIO(image_bytes)
        image = Image.open(image_stream)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image = image.resize((depth_height, depth_width))
        
        fig, axs = plt.subplots(1, 1, figsize=(10, 7))
        axs.imshow(image)
        axs.axis('off')
        
        image_folder = paths['rgb']
        curr_image_files = len(glob.glob(f'{image_folder}/*.jpg'))
        plt.savefig(f'{image_folder}/{curr_image_files+1}.jpg')
        plt.close()
                
        # axs[1].imshow(image)
                
    # plt.savefig('foo.png')
    # plt.close()
        

async def receive(websocket):
    received_data = await websocket.recv()
    try:
        data_json = json.loads(received_data)
        rgb_depth_analyser(data_json)
        
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
    for key, path in paths.items():
        path = pathlib.Path(path)
        path.mkdir(parents=True, exist_ok=True)

    asyncio.run(main())