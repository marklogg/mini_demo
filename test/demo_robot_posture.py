import asyncio

from mini.apis.api_observe import ObserveRobotPosture, RobotPosture
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_observefallclimb_pb2 import ObserveFallClimbResponse
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


# 测试,姿态检测
async def test_ObserveRobotPosture():
    """监听机器人姿态demo

    监听机器人姿态变化事件，机器上报当前的姿态RobotPosture(当发生姿态发生改变的时候)

    当机器人侧躺(LYING)或平躺(LYINGDOWN)时，停止监听，并播报"我摔倒了"

    # ObserveFallClimbResponse.status

    #     STAND = 1; //站立

    #     SPLITS_LEFT = 2; //左弓步

    #     SPLITS_RIGHT = 3; //右弓步

    #     SITDOWN = 4; //坐下

    #     SQUATDOWN = 5; //蹲下

    #     KNEELING = 6; //跪下

    #     LYING = 7; //侧躺

    #     LYINGDOWN = 8; //平躺

    #     SPLITS_LEFT_1 = 9; //左劈叉

    #     SPLITS_RIGHT_2 = 10;//右劈叉

    #     BEND = 11;//弯腰

    """
    # 创建监听对象
    observer: ObserveRobotPosture = ObserveRobotPosture()

    def handler(msg: ObserveFallClimbResponse):
        print("{0}".format(msg))
        if msg.status == RobotPosture.LYING.value or msg.status == RobotPosture.LYING_DOWN.value:
            observer.stop()
            asyncio.create_task(__tts())

    observer.set_handler(handler)
    # start
    observer.start()
    await asyncio.sleep(0)


async def __tts():
    await StartPlayTTS(text="我摔倒了").execute()
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveRobotPosture())
        # 定义了事件监听对象,必须让event_loop.run_forver()
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
