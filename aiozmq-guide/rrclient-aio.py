import asyncio
import aiozmq
import zmq


@asyncio.coroutine
def go():
    """
    Request-reply client
    Connects REQ socket to tcp://localhost:5559
    Sends "Hello" to server, expects "World" back
    """

    # Create REQ socket
    socket = yield from aiozmq.create_zmq_stream(zmq.REQ, connect='tcp://localhost:5559')

    # Do 10 requests, waiting each time for a response
    for request in range(1, 11):
        socket.write([b'Hello'])
        message = yield from socket.read()
        print('Received reply {} from [{}]'.format(request, *message))


if __name__ == "__main__":
    print('Starting client...')
    asyncio.get_event_loop().run_until_complete(go())
