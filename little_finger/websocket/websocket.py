"""
https://www.runoob.com/python3/python3-multithreading.html

"""

import asyncio

from websockets import connect
from threading import Thread


async def listen(url, callback) -> None:
    """
    listen url and consumer message
    :param url: url you want to listen
    :param callback: consumer function to handle the message
    :return:
    """
    async with connect(url) as websocket:
        while True:
            message = await websocket.recv()
            if callback:
                callback(message)


def async_listen(url, callback) -> Thread:

    def func(url_, callback_):
        asyncio.get_event_loop().run_until_complete(
            listen(url_, callback_)
        )

    t = Thread(
        name=f'Thread-{url}',
        target=func,
        args=(url, callback)
    )
    t.start()
    return t


if __name__ == '__main__':
    from datetime import datetime

    print("start")
    t = async_listen("wss://stream.binance.us:9443/stream?streams=btcusdt@miniTicker/ethusdt@miniTicker",
                     lambda x: print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + x))
    print("end")

