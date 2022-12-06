import asyncio
from datetime import datetime
import websockets

all_clients = []
msg_id = 0


async def send_message(message: str):
    for client in all_clients:
        await client.send(message)


async def new_client_connected(client_socket, path):
    print("Подключился новый чел")
    all_clients.append(client_socket)

    while True:
        new_message = await client_socket.recv()
        author = await client_socket.recv()
        print(f"{author} отправил сообщение: {new_message}")
        global msg_id
        msg_id+=1
        await send_message(message=author + f':[{msg_id}]' + new_message+"\tВремя: "+str(datetime.now()))


async def start_server():
    await websockets.serve(new_client_connected, "localhost", 8088)


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(start_server())
    event_loop.run_forever()
