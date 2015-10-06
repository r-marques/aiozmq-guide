import sys
import time
import asyncio
import aiozmq
import zmq


@asyncio.coroutine
def go():
    """
    Task sink
    Binds PULL socket to tcp://localhost:5558
    Collects results from workers via that socket
    """

    # create PULL socket to receive messages on
    receiver = yield from aiozmq.create_zmq_stream(zmq.PULL, bind='tcp://*:5558')

    # Wait for start of batch
    s = yield from receiver.read()

    # Start our clock now
    tstart = time.time()

    # Process 100 confirmations
    total_msec = 0
    for task_nbr in range(100):
        s = yield from receiver.read()
        sys.stdout.write(':') if task_nbr % 10 == 0 else sys.stdout.write('.')
        sys.stdout.flush()

    # Calculate and report duration of batch
    tend = time.time()
    print('Total elapsed time: {} msec'.format((tend - tstart) * 1000))


if __name__ == "__main__":
    print('Starting sink...')
    asyncio.get_event_loop().run_until_complete(go())
