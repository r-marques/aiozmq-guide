import asyncio
import aiozmq
import zmq


from random import randrange

@asyncio.coroutine
def go():
    """
    Weather update server
    Binds PUB socket to tcp://*:5556
    Publishes random weather updates
    """

    # create PUB socket
    pub = yield from aiozmq.create_zmq_stream(zmq.PUB, bind='tcp://*:5556')

    while True:
        zipcode = randrange(1, 100000)
        temperature = randrange(-80, 135)
        relhumidity = randrange(10, 60)

        pub.write([bytes("{} {} {}".format(zipcode, temperature, relhumidity), 'utf-8')])


if __name__ == "__main__":
    print('Starting server...')
    asyncio.get_event_loop().run_until_complete(go())
