from aiofile import async_open
from aiopath import AsyncPath
import asyncio
from datetime import datetime
import logging
import names
import websockets
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

from exchange import main as exchange

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]


    async def logging_exchange(self, message):
        dt = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        log_message = f'{dt} - {message}'
        log_file = AsyncPath('exchange_log.txt')
        async with async_open(log_file, mode='a') as f:
            await f.write(f'{log_message}\n')


    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:            
            if message.strip().startswith('exchange'):
                await self.logging_exchange(message)
                args = message.strip().removeprefix('exchange').split()
                result = await exchange(*args)
                await self.send_to_clients(f"{ws.name}: {result}")
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)
            logging.info(f'{ws.remote_address} closed.')


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
