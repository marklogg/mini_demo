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


# Test text synthesis sound
async def test_play_tts():
    """Test play tts

     Make the robot start playing a tts, the content is "Hello, I am Alphamini, la la la", and wait for the result

     #ControlTTSResponse.isSuccess: Is it successful

     #ControlTTSResponse.resultCode: Return code

    """
    # is_serial: Serial execution
    # text: The text to be synthesized
    block: StartPlayTTS = StartPlayTTS(text="Hello, I am Alphamini, la la la")
    # Return a tuple, response is a ControlTTSResponse
    (resultType, response) = await block.execute()

    print(f'test_play_tts result: {response}')
    # The response of  StartPlayTTS block contains resultCode and isSuccess
    # If resultCode !=0, you can query the error description information through errors.get_speech_error_str(response.resultCode))
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'


async def test_stop_play_tts():
    """Test stop playing tts

     Make the robot start to play a long text tts, the content is "Hello, I am Alphamini, la la la la la la la la la la la la la la la la la la la la la la la", do not wait result
     After 2s, make the robot stop playing tts

     #ControlTTSResponse.isSuccess: Is it successful

     #ControlTTSResponse.resultCode: Return code

     """
    # is_serial: Serial execution
    # text: The text to be synthesized
    block: StartPlayTTS = StartPlayTTS(is_serial=False,
                                       text="Hello, I am Alphamini, la la la la la la la la la la la la la la la la la la la la la la la")
    # Return bool to indicate whether the transmission was successful
    await block.execute()

    await asyncio.sleep(2)

    (resultType, response) = await StopPlayTTS().execute()

    print(f'test_stop_play_tts result: {response}')
    # The response of StopPlayTTS block contains resultCode and isSuccess
    # If resultCode !=0, you can query the error description information through errors.get_speech_error_str(response.resultCode))
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_stop_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_stop_play_tts result unavailable'
    assert response.isSuccess, 'test_stop_play_tts failed'


# Test playback sound (online)
async def test_play_online_audio():
    """Test playing online sound

     Make the robot play an online sound effect, such as "http://hao.haolingsheng.com/ring/000/995/52513bb6a4546b8822c89034afb8bacb.mp3"

     Supported formats are mp3, amr, wav, etc.

     And wait for the result

     #PlayAudioResponse.isSuccess: Is it successful

     #PlayAudioResponse.resultCode: Return code

    """
    # Play sound effects, url indicates the list of sound effects to be played
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
    """Test playing local sound

     Make the robot play a local built-in sound effect, the sound effect name is "read_016", and wait for the result

     #PlayAudioResponse.isSuccess: Is it successful

     #PlayAudioResponse.resultCode: Return code
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


# Test to obtain the sound resources of the robot
async def test_get_audio_list():
    """Test to get a list of sound effects

     Get the list of sound effects built into the robot and wait for the result

     #GetAudioListResponse.audio ([Audio]): Audio effect list

         #Audio.name: Audio effect name

         #Audio.suffix: audio suffix

     #GetAudioListResponse.isSuccess: Is it successful

     #GetAudioListResponse.resultCode: Return code

    """
    # search_type: AudioSearchType.INNER refers to the unmodifiable sound effect built into the robot, AudioSearchType.CUSTOM is placed in the sdcard/customize/music directory and can be modified by the developer
    block: FetchAudioList = FetchAudioList(search_type=AudioSearchType.INNER)
    # response is a GetAudioListResponse
    (resultType, response) = await block.execute()

    print(f'test_get_audio_list result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_get_audio_list timetout'
    assert response is not None and isinstance(response, GetAudioListResponse), 'test_play_audio result unavailable'
    assert response.isSuccess, 'test_get_audio_list failed'


# Test stop the tts being played
async def test_stop_audio_tts():
    """Test stop all audio being played

     Play a period of tts first, after 3s, stop all sound effects, and wait for the result

     #StopAudioResponse.isSuccess: Is it successful　

     #StopAudioResponse.resultCode: Return code

    """
    # Set is_serial=False, which means that you only need to send the instruction to the robot, and await does not need to wait for the robot to finish executing the result before returning
    block: StartPlayTTS = StartPlayTTS(is_serial=False,
                                       text="You let me say, let me say, don't interrupt me, don't interrupt me, don't interrupt me")
    response = await block.execute()
    print(f'test_stop_audio.play_tts: {response}')
    await asyncio.sleep(3)

    # Stop all sounds
    block: StopAllAudio = StopAllAudio()
    (resultType, response) = await block.execute()

    print(f'test_stop_audio:{response}')

    block: StartPlayTTS = StartPlayTTS(
        text="The second time, you let me say, let me say, don’t interrupt me, don’t interrupt me, don’t interrupt me")
    asyncio.create_task(block.execute())
    print(f'test_stop_audio.play_tts: {response}')
    await asyncio.sleep(3)

    assert resultType == MiniApiResultType.Success, 'test_stop_audio timetout'
    assert response is not None and isinstance(response, StopAudioResponse), 'test_stop_audio result unavailable'
    assert response.isSuccess, 'test_stop_audio failed'


# Test, change the volume of the robot
async def test_change_robot_volume():
    """Adjust the robot volume demo

     Set the robot volume to 0.5 and wait for the reply result

     #ChangeRobotVolumeResponse.isSuccess: Is it successful

     #ChangeRobotVolumeResponse.resultCode: Return code
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
