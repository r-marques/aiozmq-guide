import asyncio
import aiozmq
import zmq


@asyncio.coroutine
def go():
    """
    Hello World server in Python3 with aiozmq
    Binds REP socket to tcp://*:5555
    Expects b"Hello" from client, replies with b"World"
    """

    # create REP socket
    rep = yield from aiozmq.create_zmq_stream(zmq.REP, bind='tcp://*:5555')

    while True:
        # wait for next message
        message = yield from rep.read()
        print('Received request: {}'.format(*message))

        # Do some work
        yield from asyncio.sleep(1)

        # Send reply back to the client
        rep.write([b"World"])


if __name__ == "__main__":
    print('Starting server...')
    asyncio.get_event_loop().run_until_complete(go())
