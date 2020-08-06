import asyncio

from mini.apis import errors
from mini.apis.api_sound import ChangeRobotVolume, ChangeRobotVolumeResponse
from mini.apis.api_sound import FetchAudioList, GetAudioListResponse, AudioSearchType
from mini.apis.api_sound import PlayAudio, PlayAudioResponse, AudioStorageType
# from mini.apis.api_sound import PlayOnlineMusic, MusicResponse
from mini.apis.api_sound import StartPlayTTS, StopPlayTTS, ControlTTSResponse
from mini.apis.api_sound import StopAllAudio, StopAudioResponse
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


# 测试text合成声音
async def test_play_tts():
    """测试播放tts

    使机器人开始播放一段tts，内容为"你好， 我是悟空， 啦啦啦"，并等待结果

    #ControlTTSResponse.isSuccess : 是否成功

    #ControlTTSResponse.resultCode : 返回码

    """
    # is_serial:串行执行
    # text:要合成的文本
    block: StartPlayTTS = StartPlayTTS(text="你好， 我是悟空， 啦啦啦")
    # 返回元组, response是个ControlTTSResponse
    (resultType, response) = await block.execute()

    print(f'test_play_tts result: {response}')
    # StartPlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'


async def test_stop_play_tts():
    """测试停止播放tts

    使机器人开始播放一段长文本tts，内容为"你好， 我是悟空， 啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦"，不等待结果
    2s后，使机器人停止播放tts

    #ControlTTSResponse.isSuccess : 是否成功

    #ControlTTSResponse.resultCode : 返回码

    """
    # is_serial:串行执行
    # text:要合成的文本
    block: StartPlayTTS = StartPlayTTS(is_serial=False, text="你好， 我是悟空， 啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦")
    # 返回bool 表示是否发送成功
    await block.execute()

    await asyncio.sleep(2)

    (resultType, response) = await StopPlayTTS().execute()

    print(f'test_stop_play_tts result: {response}')
    # StopPlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_stop_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_stop_play_tts result unavailable'
    assert response.isSuccess, 'test_stop_play_tts failed'


# 测试播放音效(在线)
async def test_play_online_audio():
    """测试播放在线音效

    使机器人播放一段在线音效，例如"http://hao.haolingsheng.com/ring/000/995/52513bb6a4546b8822c89034afb8bacb.mp3"

    支持格式有mp3,amr,wav 等

    并等待结果

    #PlayAudioResponse.isSuccess : 是否成功

    #PlayAudioResponse.resultCode : 返回码

    """
    # 播放音效, url表示要播放的音效列表
    block: PlayAudio = PlayAudio(
        url="http://hao.haolingsheng.com/ring/000/995/52513bb6a4546b8822c89034afb8bacb.mp3",
        storage_type=AudioStorageType.NET_PUBLIC)
    # response是个PlayAudioResponse
    (resultType, response) = await block.execute()

    print(f'test_play_online_audio result: {response}')
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_online_audio timetout'
    assert response is not None and isinstance(response, PlayAudioResponse), 'test_play_online_audio result unavailable'
    assert response.isSuccess, 'test_play_online_audio failed'


async def test_play_local_audio():
    """测试播放本地音效

    使机器人播放一段本地内置音效，音效名称为"read_016"，并等待结果

    #PlayAudioResponse.isSuccess : 是否成功

    #PlayAudioResponse.resultCode : 返回码

    """

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
    """测试获取音效列表

    获取机器人内置的音效列表，并等待结果

    #GetAudioListResponse.audio ([Audio]) : 音效列表

        #Audio.name : 音效名

        #Audio.suffix : 音效后缀

    #GetAudioListResponse.isSuccess : 是否成功

    #GetAudioListResponse.resultCode : 返回码

    """
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
    """测试停止所有正在播放的音频

    先播放一段tts，3s后，停止所有所有音效，并等待结果

    #StopAudioResponse.isSuccess : 是否成功　

    #StopAudioResponse.resultCode : 返回码

    """
    # 设置is_serial=False, 表示只需将指令发送给机器人,await不需要等机器人执行完结果再返回
    block: StartPlayTTS = StartPlayTTS(is_serial=False, text="你让我说，让我说，不要打断我，不要打断我，不要打断我")
    response = await block.execute()
    print(f'test_stop_audio.play_tts: {response}')
    await asyncio.sleep(3)

    # 停止所有声音
    block: StopAllAudio = StopAllAudio()
    (resultType, response) = await block.execute()

    print(f'test_stop_audio:{response}')

    block: StartPlayTTS = StartPlayTTS(text="第二次, 你让我说，让我说，不要打断我，不要打断我，不要打断我")
    asyncio.create_task(block.execute())
    print(f'test_stop_audio.play_tts: {response}')
    await asyncio.sleep(3)

    assert resultType == MiniApiResultType.Success, 'test_stop_audio timetout'
    assert response is not None and isinstance(response, StopAudioResponse), 'test_stop_audio result unavailable'
    assert response.isSuccess, 'test_stop_audio failed'


# 测试, 改变机器人的音量
async def test_change_robot_volume():
    """调整机器人音量demo

    设置机器人音量为0.5，等待回复结果

    #ChangeRobotVolumeResponse.isSuccess : 是否成功

    #ChangeRobotVolumeResponse.resultCode : 返回码

    """
    # volume: 0~1.0
    block: ChangeRobotVolume = ChangeRobotVolume(volume=0.5)
    # response:ChangeRobotVolumeResponse
    (resultType, response) = await block.execute()

    print(f'test_change_robot_volume result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_change_robot_volume timetout'
    assert response is not None and isinstance(response,
                                               ChangeRobotVolumeResponse), 'test_change_robot_volume result unavailable'
    assert response.isSuccess, 'get_action_list failed'


async def main():
    device: WiFiDevice = await test_get_device_by_name()
    if device:
        await test_connect(device)
        await test_start_run_program()
        await test_play_tts()
        await test_stop_play_tts()
        await test_get_audio_list()
        await test_play_local_audio()
        await test_play_online_audio()
        await test_stop_audio_tts()
        await test_change_robot_volume()
        await shutdown()


if __name__ == '__main__':
    asyncio.run(main())
