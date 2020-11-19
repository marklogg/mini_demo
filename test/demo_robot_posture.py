import asyncio

from mini.apis.api_observe import ObserveRobotPosture, RobotPosture
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_observefallclimb_pb2 import ObserveFallClimbResponse
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


# 测试,姿态检测
async def test_ObserveRobotPosture():
    """Monitor robot posture demo

     Monitor robot posture change events, and the machine reports the current posture RobotPosture (when the posture changes)

     When the robot is lying on its side (LYING) or lying down (LYINGDOWN), stop monitoring and announce "I fell"

     # ObserveFallClimbResponse.status

     # STAND = 1; //Stand

     # SPLITS_LEFT = 2; //Left lunge

     # SPLITS_RIGHT = 3; //Right lunge

     # SITDOWN = 4; //Sit down

     # SQUATDOWN = 5; //Squat down

     # KNEELING = 6; //Kneel down

     # LYING = 7; //Lying on your side

     # LYINGDOWN = 8; //Lying down

     # SPLITS_LEFT_1 = 9; //Left split

     # SPLITS_RIGHT_2 = 10;//Right split

     # BEND = 11;//Bent over
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
    await StartPlayTTS(text="Oh, I fell").execute()
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveRobotPosture())
        # The event listener object is defined, and event_loop.run_forver() must be
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
