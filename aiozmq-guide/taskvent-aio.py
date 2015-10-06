import random
import asyncio
import aiozmq
import zmq


@asyncio.coroutine
def go():
    """
    Task ventilator
    Binds PUSH socket to tcp://localhost:5557
    Sends batch of tasks to workers via that socket
    """

    # create PUSH socket to send messages on
    sender = yield from aiozmq.create_zmq_stream(zmq.PUSH, bind='tcp://*:5557')

    # create PUSH socket with direct access to the sink:
    # used to syncronize start of batch
    sink = yield from aiozmq.create_zmq_stream(zmq.PUSH, connect='tcp://localhost:5558')

    print('Press Enter when the workers are ready: ')
    _ = input()
    print('Sending tasks to workers...')

    # The first message is "0" and signals start of batch
    sink.write([b'0'])

    # Initialize random number generator
    random.seed()

    # Send 100 tasks
    total_msec = 0
    for task_nbr in range(100):
        # Random workload from 1 to 100 msecs
        workload = random.randint(1, 100)
        total_msec += workload

        sender.write([bytes('{}'.format(workload), 'utf-8')])

    print('Total expected cost: {} msec'.format(total_msec))

    # Give ZMQ time to deliver
    yield from sender.drain()


if __name__ == "__main__":
    print('Starting taskvent...')
    asyncio.get_event_loop().run_until_complete(go())
