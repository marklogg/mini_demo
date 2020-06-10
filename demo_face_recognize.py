import asyncio

from mini.blockapi.block_observe import ObserveFaceRecognise
from mini.blockapi.block_sound import PlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_facerecognisetask_pb2 import FaceRecogniseTaskResponse
from test_connect import test_connect, shutdown
from test_connect import test_get_device_by_name, test_start_run_program


# 测试, 检测到注册的人脸,则上报事件, 如果陌生人,返回"stranger"
async def test_ObserveFaceRecognise():
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
    await PlayTTS(text=f'你好， {name}').execute()
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveFaceRecognise())
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
