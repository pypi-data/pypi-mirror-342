import asyncio
import json
import websockets
import cv2
import base64
import numpy as np

class VISAsyncClient:
    def __init__(self, server_uri="ws://<server-ip>:8765"):
        self.server_uri = server_uri
        self.websocket = None
        self.results = {}
        self.response_queue = asyncio.Queue()

    async def connect(self):
        if self.websocket is None:
            self.websocket = await websockets.connect(self.server_uri)
            asyncio.create_task(self.listen_for_results())

    async def listen_for_results(self):
        while True:
            try:
                response = await self.websocket.recv()
                data = json.loads(response)

                if "image" in data:
                    img_base64 = data["image"]
                    try:
                        img_data = base64.b64decode(img_base64)
                        np_arr = np.frombuffer(img_data, np.uint8)
                        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                        data["image"] = img
                    except Exception as e:
                        print("Error decoding image:", e)
                        data["image"] = None

                module_name = data.get("module", "unknown")
                self.results[module_name] = data
                await self.response_queue.put(data)
            except websockets.ConnectionClosed:
                print("Connection lost. Reconnecting...")
                self.websocket = None
                await self.connect()
                break

    async def load_module(self, module_name):
        await self.connect()
        request = {"command": f"{module_name}_load"}
        await self.websocket.send(json.dumps(request))

    async def run_module(self, module_name, prompt=None, bbox=None, mask=None):
        await self.connect()
        request = {"command": f"{module_name}_run"}
        if prompt:
            request["prompt"] = prompt
        if bbox:
            request["bbox"] = bbox  # Format: [x, y, w, h]
        if mask is not None:
            _, buffer = cv2.imencode('.png', mask)
            request["mask"] = base64.b64encode(buffer).decode('utf-8')
        await self.websocket.send(json.dumps(request))
        data = await self.response_queue.get()
        return data

    async def stop_module(self, module_name):
        await self.connect()
        request = {"command": f"{module_name}_stop"}
        await self.websocket.send(json.dumps(request))

    async def close(self):
        if self.websocket:
            await self.websocket.close()
