import asyncio

from mini.apis.api_observe import ObserveInfraredDistance
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_observeinfrareddistance_pb2 import ObserveInfraredDistanceResponse
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


async def test_ObserveInfraredDistance():
    """Monitor infrared distance demo

     Monitor infrared distance events, the robot reports the detected infrared distance to the nearest obstacle in front of you

     When the returned infrared distance is less than 500, stop monitoring and broadcast "Detected infrared distance xxx" (xxx is the infrared distance value)

    """
    # 红外监听对象
    observer: ObserveInfraredDistance = ObserveInfraredDistance()

    # 定义处理器
    # ObserveInfraredDistanceResponse.distance
    def handler(msg: ObserveInfraredDistanceResponse):
        print("distance = {0}".format(str(msg.distance)))
        if msg.distance < 500:
            observer.stop()
            asyncio.create_task(__tts(msg.distance))

    observer.set_handler(handler)
    observer.start()
    await asyncio.sleep(0)


async def __tts(distance: int):
    result = await StartPlayTTS(text=f"Detected infrared distance {distance}").execute()
    print(f"tts over {result}")
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveInfraredDistance())
        # The event listener object is defined, and event_loop.run_forver() must be
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
