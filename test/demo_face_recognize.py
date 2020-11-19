import asyncio

from mini.apis.api_observe import ObserveFaceRecognise
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_facerecognisetask_pb2 import FaceRecogniseTaskResponse
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


# Test, if the registered face is detected, the incident will be reported, if it is a stranger, it will return "stranger"
async def test_ObserveFaceRecognise():
    """Face recognition demo

     Monitor face recognition events, and the robot reports the recognized face information (array)

     If it is a registered face, return face details: id, name, gender, age

     If it is a stranger, return name: "stranger"

     When the face is successfully recognized, stop monitoring and broadcast "Hello, xxx" (xxx is the name in the face information)

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
    await StartPlayTTS(text=f'hello ， {name}').execute()
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveFaceRecognise())
        # The event listener object is defined, and event_loop.run_forver() must be
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
