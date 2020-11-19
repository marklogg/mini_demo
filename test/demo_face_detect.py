import asyncio

from mini.apis.api_observe import ObserveFaceDetect
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_facedetecttask_pb2 import FaceDetectTaskResponse
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


async def test_ObserveFaceDetect():
    """Face count detection demo

     Detection of the number of faces, if faces are detected, the incident is reported

     When the number of faces detected is greater than or equal to 1, stop monitoring and broadcast "There seems to be xx faces in front of me" (xx is the number of faces)

    """
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
    await StartPlayTTS(text=f'There seems to be {count} people in front of me').execute()
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveFaceDetect())
        # The event listener object is defined, and event_loop.run_forver() must be
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
