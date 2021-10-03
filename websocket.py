import asyncio
import websockets
import json

#TODO identify 과정 추가

class Websocket:
    def __init__(self, BOT_TOKEN):
        self.TOKEN = BOT_TOKEN

    def start(self):
        asyncio.run(self.connect())

    async def connect(self):
        async with websockets.connect("wss://gateway.discord.gg") as self.ws:
            await self.handler()

    async def identify(self):
        data = {
            "op": 2,
            'd': {
                "token": self.TOKEN,
                "intents": 513,
                "properties": {
                "$os": "linux",
                "$browser": "my_library",
                "$device": "my_library"
                }
            }
        }
        data = json.dumps(data)

        print("identifying")
        await self.ws.send(data)

    async def handler(self):
        await self.identify()
        while True:
            msg = await self.ws.recv()
            msg = json.loads(msg)
            await self.consumer(msg)

    async def consumer(self, msg):
        op = msg["op"]

        if op == 0: # Dispatch
            self.opcode0(msg)
        elif op == 7: # Reconnect
            print(msg)
        elif op == 9: # Invalid Session
            print(msg)
        elif op == 10: # Hello
            self.interval = int(msg['d']["heartbeat_interval"])/1000
            asyncio.create_task(self.heartbeat())
        elif op == 11: #Heartbeat ACK
            asyncio.create_task(self.heartbeat())
        else:
            print(msg)

    def opcode0(self, msg):
        if msg['t'] == "MESSAGE_CREATE":
            print(msg['d']['content'])
        else:
            print(msg)

    async def heartbeat(self):
        await asyncio.sleep(self.interval)

        data = {
            "op": 1,
            'd': None
        }
        data = json.dumps(data)

        print("send Heartbeat")
        await self.ws.send(data)
