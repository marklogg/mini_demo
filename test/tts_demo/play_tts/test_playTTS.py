import asyncio

from mini import mini_sdk
from mini.apis.api_setup import StartRunProgram
from mini.apis.api_sound import PlayTTS, TTSControlType, ControlTTSResponse
from mini.apis.base_api import MiniApiResultType
from mini.mini_sdk import WiFiDevice


async def play_tts():
    block: PlayTTS = PlayTTS(text="你好， 我是悟空，测试测试，啦啦啦", control_type=TTSControlType.START)
    # 返回元组, response是个ControlTTSResponse
    (resultType, response) = await block.execute()

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'


def main():
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(mini_sdk.get_device_by_name("0090", 10))
    if device:
        asyncio.get_event_loop().run_until_complete(mini_sdk.connect(device))
        asyncio.get_event_loop().run_until_complete(StartRunProgram().execute())
        asyncio.get_event_loop().run_until_complete(asyncio.sleep(6))
        asyncio.get_event_loop().run_until_complete(play_tts())
        asyncio.get_event_loop().run_until_complete(mini_sdk.release())
