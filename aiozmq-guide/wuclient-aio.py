import sys
import asyncio
import aiozmq
import zmq


@asyncio.coroutine
def go(zip_filter):
    """
    Weather update client
    Connects SUB socket to tcp://localhost:5556
    Collects weather updates and finds avg temp in zipcode
    """

    # create SUB socket
    sub = yield from aiozmq.create_zmq_stream(zmq.SUB, connect='tcp://localhost:5556')
    sub.transport.subscribe(bytes(zip_filter, 'utf-8'))

    # Process 5 updates
    total_temp = 0
    for update_nbr in range(5):
        string = yield from sub.read()
        zipcode, temperature, relhumidity = string[0].split()
        print('Received update [{}] {} {} {}'.format(update_nbr, zipcode, temperature, relhumidity))
        total_temp += int(temperature)

    print("Average temperature for zipcode '{}' was {}".format(zip_filter, total_temp / update_nbr))


if __name__ == "__main__":
    print('Collection updates from weather server...')
    zip_filter = sys.argv[1] if len(sys.argv) > 1 else '10001'
    asyncio.get_event_loop().run_until_complete(go(zip_filter))
    
