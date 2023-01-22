import uuid
import queue
import signal
import random
import asyncio
import threading
import websockets

ALLOWED = set(['😂', '🤪', '😘'])
CLIENTS = set()
QUEUE = queue.Queue(maxsize=1000) # Don't bother with more

IS_EXITING = False
LOCK = threading.Lock()

async def send(websocket, message):
    try:
        await websocket.send(message)
    except websockets.ConnectionClosed:
        pass

async def monitor_queue():
    while True:
        if not IS_EXITING:
            try:
                message = QUEUE.get(timeout = 1)
            except queue.Empty:
                continue
            client_subset = random.sample(list(CLIENTS), min(4, len(CLIENTS)))
            websockets.broadcast(client_subset, message)
        else:
            return

def monitor_queue_callback():
    queue_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(queue_loop)
    queue_loop.run_until_complete(monitor_queue())
    queue_loop.close()

async def receiver(websocket, path):
    client_id = uuid.uuid1()
    CLIENTS.add(websocket)
    while True:
        if not IS_EXITING:
            try:
                message = await websocket.recv()
                if message in ALLOWED:
                    QUEUE.put(message)
            except websockets.ConnectionClosed:
                try:
                    CLIENTS.remove(websocket)
                except KeyError:
                    continue
        else:
            return

async def main():
    async with websockets.serve(receiver, host = "0.0.0.0", port = 8765, origins = ["https://mattwie.se"]):
        print("WebSocket server running")
        await asyncio.Future()

T1 = threading.Thread(target=monitor_queue_callback)
T1.start()
print("Queue monitor thread started")

def handler(signum, frame):
    global T1
    global T2
    global LOCK
    global LOOP
    global IS_EXITING

    print()
    print("Acquiring lock")
    LOCK.acquire()
    print("Lock acquired, performing cleanup")
    IS_EXITING = True
    LOCK.release()
    T1.join()

    print("Goodbye")
    exit(1)

signal.signal(signal.SIGINT, handler)

asyncio.run(main())
