import asyncio

from websockets import connect


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


if __name__ == '__main__':
    from datetime import datetime

    asyncio.get_event_loop().run_until_complete(
        listen(
            "wss://stream.binance.us:9443/stream?streams=btcusdt@miniTicker/ethusdt@miniTicker",
            lambda x: print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + x)
        )
    )
