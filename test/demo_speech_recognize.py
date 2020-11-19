import asyncio

from mini.apis.api_observe import ObserveSpeechRecognise
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_speechrecognise_pb2 import SpeechRecogniseResponse
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


async def __tts():
    block: StartPlayTTS = StartPlayTTS(text="Hello, I am alphamini, Lalila, Lalila")
    response = await block.execute()
    print(f'tes_play_tts: {response}')


# Test ,monitor speech recognition
async def test_speech_recognise():
    """Monitor voice recognition demo

     Monitor voice recognition events, and the robot reports the text after voice recognition

     When the voice is recognized as "hello", broadcast "Hello, I am alphamini, Lalila, Lalila"

     When the voice is recognized as "stop", stop monitoring

    # SpeechRecogniseResponse.text

    # SpeechRecogniseResponse.isSuccess

    # SpeechRecogniseResponse.resultCode

    """
    # 语音监听对象
    observe: ObserveSpeechRecognise = ObserveSpeechRecognise()

    # 处理器
    # SpeechRecogniseResponse.text
    # SpeechRecogniseResponse.isSuccess
    # SpeechRecogniseResponse.resultCode
    def handler(msg: SpeechRecogniseResponse):
        print(f'=======handle speech recognise:{msg}')
        print("{0}".format(str(msg.text)))
        if str(msg.text).lower() == "hello":
            # "hello" is monitored, tts say hello
            asyncio.create_task(__tts())

        elif str(msg.text).lower() == "stop":
            # Listen "stop", stop monitoring
            observe.stop()
            # stop event_loop
            asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)

    observe.set_handler(handler)
    # start
    observe.start()
    await asyncio.sleep(0)


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_speech_recognise())
        # The event listener object is defined, and event_loop.run_forver() must be
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
