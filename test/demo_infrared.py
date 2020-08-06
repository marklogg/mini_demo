import asyncio

from mini.apis.api_observe import ObserveInfraredDistance
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_observeinfrareddistance_pb2 import ObserveInfraredDistanceResponse
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


async def test_ObserveInfraredDistance():
    """监听红外距离demo

    监听红外距离事件，机器人上报检测到的与面前最近障碍物的红外距离

    当返回的红外距离小于500，停止监听，并播报"检测到红外距离xxx"(xxx是红外距离数值)

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
    result = await StartPlayTTS(text=f"检测到红外距离{distance}").execute()
    print(f"tts over {result}")
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveInfraredDistance())
        # 定义了事件监听对象,必须让event_loop.run_forver()
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
