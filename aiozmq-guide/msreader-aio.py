import asyncio
import aiozmq
import zmq
import time


@asyncio.coroutine
def go():
    """
    Reading from multiple sockets
    This version uses a simple recv loop
    """

    # create PULL socket. Connecs to task ventilator
    receiver = yield from aiozmq.create_zmq_stream(zmq.PULL, connect='tcp://localhost:5557')

    # create SUB socket. Connect to weather server
    subscriber = yield from aiozmq.create_zmq_stream(zmq.SUB, connect='tcp://localhost:5556')
    subscriber.transport.subscribe(b'10001')

    # Process messages from both sockets
    # We prioritize traffic from the task ventilator
    # TODO: Check if its possible to prioritize with asyncio
    while True:
        # Process any waiting tasks
        msg = yield from receiver.read()
        # process task
        print(*msg)

        # Process any waiting weather updates
        msg = yield from subscriber.read()
        # process weather update
        print(*msg)

        # No activity, so sleep for 1 msec
        yield from asyncio.sleep(0.001)


if __name__ == "__main__":
    print('Waiting for tasks and weather updates...')
    asyncio.get_event_loop().run_until_complete(go())
