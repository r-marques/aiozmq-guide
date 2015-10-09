import asyncio
import aiozmq
import zmq


@asyncio.coroutine
def go():
    """
    Request-reply service
    Connects REP socket to tcp://localhost:5560
    Expects "Hello" from client, replies with "World"
    """

    # create REP socket
    socket = yield from aiozmq.create_zmq_stream(zmq.REP, connect='tcp://localhost:5560')

    while True:
        message = yield from socket.read()
        print('Received request: {}'.format(*message))
        socket.write([b'World'])


if __name__ == "__main__":
    print('Starting worker...')
    asyncio.get_event_loop().run_until_complete(go())
