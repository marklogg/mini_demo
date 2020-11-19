import asyncio

from mini.apis.api_observe import ObserveSpeechRecognise
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_speechrecognise_pb2 import SpeechRecogniseResponse
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


async def __tts():
    block: StartPlayTTS = StartPlayTTS(text="你好， 我是悟空， 啦里啦，啦里啦")
    response = await block.execute()
    print(f'tes_play_tts: {response}')


# 测试监听语音识别
async def test_speech_recognise():
    """监听语音识别demo

    监听语音识别事件，机器人上报语音识别后的文字

    当识别到语音为"悟空"时，播报"你好， 我是悟空， 啦里啦，啦里啦"

    当识别到语音为"结束"时，停止监听

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

        # if str(msg.text)[-1].isalpha() is False:
        #     if str(msg.text)[:-1].lower() == "Hello":
        #         asyncio.create_task(__tts())

        if str(msg.text).lower() == "悟空":
            # 监听到"悟空", tts打个招呼
            asyncio.create_task(__tts())

        elif str(msg.text).lower() == "结束":
            # 监听到结束, 停止监听
            observe.stop()
            # 结束event_loop
            asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)

    observe.set_handler(handler)
    # 启动
    observe.start()
    await asyncio.sleep(0)


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_speech_recognise())
        # 定义了事件监听对象,必须让event_loop.run_forver()
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
