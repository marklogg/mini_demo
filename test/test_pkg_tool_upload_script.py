import mini
import mini.pkg_tool as pt

device = "0717"

py_script_tts = """import asyncio
import mini
from mini.apis import errors
from mini.apis.api_sound import StartPlayTTS, ControlTTSResponse
from mini.apis.base_api import MiniApiResultType


# 测试text合成声音
async def test_play_tts():
	wifiDevice = mini.WiFiDevice(port=8800)
	sdk_connect = await mini.mini_sdk.connect(wifiDevice)
	print('connect device {0} {1}'.format(wifiDevice, sdk_connect))
	if not sdk_connect:
		print("connect failed.......................")
		return
	await mini.mini_sdk.enter_program()
	# text:要合成的文本
	block: StartPlayTTS = StartPlayTTS(text="两间公司合并后，新公司将以Cenovus名称继续营运，总部维持于加拿大艾伯塔省卡尔加里。交易已获赫斯基能源公司与Cenovus公司双方董事局一致通过，预期将于明年第一季度完成交易。根据安排协议条款，赫斯基能源股东将会收取0.7845股Cenovus普通股，以及可认购0.0651股Cenovus普通股的认股权证，交换所拥有的每股赫斯基能源普通股。预期交易完成后及行使任何认股权证前，Cenovus股东将拥有合并公司约60.775%股权，赫斯基能源股东则占约39.225%股权。")
	# 返回元组, response是个ControlTTSResponse
	(resultType, response) = await block.execute()

	print(f'test_play_tts result: {response}')
	# StartPlayTTS block的response包含resultCode和isSuccess
	# 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
	print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

	assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
	assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
	assert response.isSuccess, 'test_play_tts failed'

	await mini.mini_sdk.quit_program()


async def main():
	await test_play_tts()


if __name__ == '__main__':
	asyncio.run(main())"""

py_script_dance = """import asyncio

import mini
from mini.apis import errors
from mini.apis.api_behavior import StartBehavior
from mini.apis.base_api import MiniApiResultType
from mini.pb2.codemao_controlbehavior_pb2 import ControlBehaviorResponse


# 测试text合成声音
async def test_control_behavior():
    wifiDevice = mini.WiFiDevice(port=8800)
    sdk_connect = await mini.mini_sdk.connect(wifiDevice)
    print('connect device {0} {1}'.format(wifiDevice, sdk_connect))
    if not sdk_connect:
        print("connect failed.......................")
        return
    await mini.mini_sdk.enter_program()
    # text:要合成的文本
    block: StartBehavior = StartBehavior(name="012")
    # 返回元组, response是个ControlTTSResponse
    (resultType, response) = await block.execute()

    print(f'test_control_behavior result: {response}')
    # StartPlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_express_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_control_behavior timetout'
    assert response is not None and isinstance(response,
                                               ControlBehaviorResponse), 'test_control_behavior result unavailable'
    assert response.isSuccess, 'control_behavior failed'

    await mini.mini_sdk.quit_program()


async def main():
    await test_control_behavior()


if __name__ == '__main__':
    asyncio.run(main())
"""

fileName = "DanceTest.py"


def test_upload_script():
    # 上传脚本到机器人
    pt.upload_script(1, device, fileName, bytes(py_script_tts, encoding="utf-8"))


def test_check_upload_script():
    # 检查脚本是否已上传到机器人
    pt.upload_script(2, device, fileName)


def test_run_upload_script():
    # 执行已上传的脚本
    pt.upload_script(3, device, fileName)


def test_stop_upload_script():
    # 执行已上传的脚本
    pt.upload_script(4, device)


def test_list_upload_script():
    # 获取已上传的脚本列表
    pt.upload_script(5, device)


async def release():
    await mini.mini_sdk.release()

if __name__ == '__main__':
    # test_upload_script()
    test_check_upload_script()
    # test_run_upload_script()
    # test_stop_upload_script()
    # test_list_upload_script()
