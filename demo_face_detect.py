import asyncio

from mini.blockapi.block_observe import ObserveFaceDetect
from mini.blockapi.block_sound import PlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_facedetecttask_pb2 import FaceDetectTaskResponse
from test_connect import test_connect, shutdown
from test_connect import test_get_device_by_name, test_start_run_program


# 人脸检测,检测到人脸,则上报事件
async def test_ObserveFaceDetect():
    observer: ObserveFaceDetect = ObserveFaceDetect()

    # FaceDetectTaskResponse.count
    # FaceDetectTaskResponse.isSuccess
    # FaceDetectTaskResponse.resultCode
    def handler(msg: FaceDetectTaskResponse):
        print(f"{msg}")
        if msg.isSuccess and msg.count:
            observer.stop()
            asyncio.create_task(__tts(msg.count))

    observer.set_handler(handler)
    observer.start()
    await asyncio.sleep(0)


async def __tts(count):
    await PlayTTS(text=f'在我面前好像有{count}个人').execute()
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveFaceDetect())
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
