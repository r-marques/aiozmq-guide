import asyncio
import aiozmq
import zmq

@asyncio.coroutine
def go():
    """
    Hello World client in Python
    Connects REQ socket to tcp://localhost:5555
    Sends "Hello" to server, expects "World" back
    """

    # create REQ socket and connect to server
    req = yield from aiozmq.create_zmq_stream(zmq.REQ, connect='tcp://localhost:5555')

    for request in range(10):
        print('Sending request {}...'.format(request))
        req.write([b"Hello"])

        # get the reply
        message = yield from req.read()
        print('Received reply {} [{}]'.format(request, *message))


if __name__ == "__main__":
    print('Starting client...')
    asyncio.get_event_loop().run_until_complete(go())
