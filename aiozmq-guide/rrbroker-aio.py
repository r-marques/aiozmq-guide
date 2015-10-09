import asyncio
import aiozmq
import zmq


@asyncio.coroutine
def go():
    """
    Simple request-reply broker
    """

    # Create ROUTER socket
    frontend = yield from aiozmq.create_zmq_stream(zmq.ROUTER, bind='tcp://*:5559')

    # Create DEALER socket
    backend = yield from aiozmq.create_zmq_stream(zmq.DEALER, bind='tcp://*:5560')

    # TODO: Check for the closest thing to a Poller with asyncio

    # Switch messages between sockets
    while True:
        # Check frontend
        message = yield from frontend.read()
        backend.write(message)

        # Check backend
        message = yield from backend.read()
        frontend.write(message)


if __name__ == "__main__":
    print('Starting broker...')
    asyncio.get_event_loop().run_until_complete(go())
