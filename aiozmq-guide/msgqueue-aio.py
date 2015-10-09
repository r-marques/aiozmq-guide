import asyncio
import aiozmq
import zmq


@asyncio.coroutine
def go():
    """
    Simple message queuing broker
    Same as request-reply broker but using QUEUE device
    """

    # Create ROUTER socket. Socket facing clients
    frontend = yield from aiozmq.create_zmq_stream(zmq.ROUTER, bind='tcp://*:5559')

    # create DEALER socket. Socket facing services
    backend = yield from aiozmq.create_zmq_stream(zmq.DEALER, bind='tcp://*:5560')

    # create QUEUE device
    #TODO: not sure that this is the best way to do it
    zmq.device(zmq.QUEUE, frontend.transport._zmq_sock, backend.transport._zmq_sock)


if __name__ == "__main__":
    print('Starting message queue...')
    asyncio.get_event_loop().run_until_complete(go())
