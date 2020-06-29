import asyncio

from mini.apis import errors
from mini.apis.api_sound import FetchAudioList, GetAudioListResponse, AudioSearchType
from mini.apis.api_sound import PlayAudio, PlayAudioResponse, AudioStorageType
from mini.apis.api_sound import PlayOnlineMusic, MusicResponse
from mini.apis.api_sound import PlayTTS, ControlTTSResponse, TTSControlType
from mini.apis.api_sound import StopAllAudio, StopAudioResponse
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


# 测试text合成声音
async def test_play_tts():
    # is_serial:串行执行
    # text:要合成的文本
    # control_type: TTSControlType.START: 播放tts; TTSControlType.STOP: 停止tts
    block: PlayTTS = PlayTTS(text="你好， 我是悟空， 啦啦啦", control_type=TTSControlType.START)
    # 返回元组, response是个ControlTTSResponse
    (resultType, response) = await block.execute()

    print(f'test_play_tts result: {response}')
    # PlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'


# 测试播放音效(在线)
async def test_play_online_audio():
    # 播放音效, url表示要播放的音效列表
    block: PlayAudio = PlayAudio(
        url="http://yun.lnpan.com/music/download/ring/000/075/5653bae83917a892589b372782175dd8.amr",
        storage_type=AudioStorageType.NET_PUBLIC)
    # response是个PlayAudioResponse
    (resultType, response) = await block.execute()

    print(f'test_play_online_audio result: {response}')
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_online_audio timetout'
    assert response is not None and isinstance(response, PlayAudioResponse), 'test_play_online_audio result unavailable'
    assert response.isSuccess, 'test_play_online_audio failed'


async def test_play_local_audio():
    # 播放音效, url表示要播放的音效列表
    block: PlayAudio = PlayAudio(
        url="read_016",
        storage_type=AudioStorageType.PRESET_LOCAL)
    # response是个PlayAudioResponse
    (resultType, response) = await block.execute()

    print(f'test_play_local_audio result: {response}')
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_local_audio timetout'
    assert response is not None and isinstance(response, PlayAudioResponse), 'test_play_local_audio result unavailable'
    assert response.isSuccess, 'test_play_local_audio failed'


# 测试获取机器人的音效资源
async def test_get_audio_list():
    # search_type: AudioSearchType.INNER 是指机器人内置的不可修改的音效, AudioSearchType.CUSTOM 是放置在sdcard/customize/music目录下可别开发者修改的音效
    block: FetchAudioList = FetchAudioList(search_type=AudioSearchType.INNER)
    # response是个GetAudioListResponse
    (resultType, response) = await block.execute()

    print(f'test_get_audio_list result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_get_audio_list timetout'
    assert response is not None and isinstance(response, GetAudioListResponse), 'test_play_audio result unavailable'
    assert response.isSuccess, 'test_get_audio_list failed'


# 测试停止正在播放的tts
async def test_stop_audio_tts():
    # 设置is_serial=False, 表示只需将指令发送给机器人,await不需要等机器人执行完结果再返回
    block: PlayTTS = PlayTTS(is_serial=False, text="你让我说，让我说，不要打断我，不要打断我，不要打断我")
    response = await block.execute()
    print(f'test_stop_audio.play_tts: {response}')
    await asyncio.sleep(3)

    # 停止所有声音
    block: StopAllAudio = StopAllAudio()
    (resultType, response) = await block.execute()

    print(f'test_stop_audio:{response}')

    assert resultType == MiniApiResultType.Success, 'test_stop_audio timetout'
    assert response is not None and isinstance(response, StopAudioResponse), 'test_stop_audio result unavailable'
    assert response.isSuccess, 'test_stop_audio failed'


# 测试停止正在播放的onlineMusic
async def test_stop_audio_online_music():
    # 设置is_serial=False, 表示只需将指令发送给机器人,await不需要等机器人执行完结果再返回
    block: PlayOnlineMusic = PlayOnlineMusic(is_serial=False, name='我的世界')
    response = await block.execute()
    print(f'test_stop_audio.play_online_music: {response}')
    await asyncio.sleep(10)

    # 停止所有声音
    block: StopAllAudio = StopAllAudio()
    (resultType, response) = await block.execute()

    print(f'test_stop_audio:{response}')

    assert resultType == MiniApiResultType.Success, 'test_stop_audio timetout'
    assert response is not None and isinstance(response, StopAudioResponse), 'test_stop_audio result unavailable'
    assert response.isSuccess, 'test_stop_audio failed'


# 测试播放一首音乐
async def test_play_online_music():
    # 播放qq音乐, 需要在手机端授权
    block: PlayOnlineMusic = PlayOnlineMusic(name='我的世界')
    (resultType, response) = await block.execute()

    print(f'test_play_online_music result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_play_online_music timetout'
    assert response is not None and isinstance(response, MusicResponse), 'test_play_online_music result unavailable'
    assert response.isSuccess, 'test_play_online_music failed'


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_play_tts())
        asyncio.get_event_loop().run_until_complete(test_get_audio_list())
        asyncio.get_event_loop().run_until_complete(test_play_local_audio())
        asyncio.get_event_loop().run_until_complete(test_play_online_audio())
        asyncio.get_event_loop().run_until_complete(test_play_online_music())
        asyncio.get_event_loop().run_until_complete(test_stop_audio_tts())
        asyncio.get_event_loop().run_until_complete(test_stop_audio_online_music())
        asyncio.get_event_loop().run_until_complete(shutdown())
