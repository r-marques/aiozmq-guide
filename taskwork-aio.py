import sys
import asyncio
import aiozmq
import zmq


@asyncio.coroutine
def go():
    """
    Task worker
    Connects PULL socket to tcp://localhost:5557
    Collects workloads from ventilator via that socket
    Connects PUSH socket to tcp://localhost:5558
    Sends results to sink via that socket
    """

    # create PULL socket to receive messages on
    receiver = yield from aiozmq.create_zmq_stream(zmq.PULL, connect='tcp://localhost:5557')

    # create PUSH socket to send messages on
    sender = yield from aiozmq.create_zmq_stream(zmq.PUSH, connect='tcp://localhost:5558')

    # Process tasks forever
    while True:
        s = yield from receiver.read()

        # Simple progress indicator for the viewer
        sys.stdout.write('.')
        sys.stdout.flush()

        # Do the work
        yield from asyncio.sleep(int(s[0]) * 0.001)

        # Send results to the sink
        sender.write([b''])


if __name__ == "__main__":
    print('Starting worker...')
    asyncio.get_event_loop().run_until_complete(go())
