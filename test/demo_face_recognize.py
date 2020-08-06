import asyncio

from mini.apis.api_observe import ObserveFaceRecognise
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_facerecognisetask_pb2 import FaceRecogniseTaskResponse
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


# 测试, 检测到注册的人脸,则上报事件, 如果陌生人,返回"stranger"
async def test_ObserveFaceRecognise():
    """人脸识别demo

    监听人脸识别事件，机器人上报识别到的人脸信息(数组)

    如果是已注册的人脸，返回人脸详细信息：id，名字，性别，年龄

    如果是陌生人，返回 name: "stranger"

    当成功识别到人脸后，停止监听，播报"你好，xxx"(xxx为人脸信息中的name)

    """
    observer: ObserveFaceRecognise = ObserveFaceRecognise()

    # FaceRecogniseTaskResponse.faceInfos: [FaceInfoResponse]
    # FaceInfoResponse.id, FaceInfoResponse.name,FaceInfoResponse.gender,FaceInfoResponse.age
    # FaceRecogniseTaskResponse.isSuccess
    # FaceRecogniseTaskResponse.resultCode
    def handler(msg: FaceRecogniseTaskResponse):
        print(f"{msg}")
        if msg.isSuccess and msg.faceInfos:
            observer.stop()
            asyncio.create_task(__tts(msg.faceInfos[0].name))

    observer.set_handler(handler)
    observer.start()
    await asyncio.sleep(0)


async def __tts(name):
    await StartPlayTTS(text=f'你好， {name}').execute()
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveFaceRecognise())
        # 定义了事件监听对象,必须让event_loop.run_forver()
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
