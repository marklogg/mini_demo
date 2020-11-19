import asyncio

from mini.apis import errors
from mini.apis.api_behavior import StartBehavior, ControlBehaviorResponse, StopBehavior
from mini.apis.api_expression import ControlMouthLamp, ControlMouthResponse
from mini.apis.api_expression import PlayExpression, PlayExpressionResponse
from mini.apis.api_expression import SetMouthLamp, SetMouthLampResponse, MouthLampColor, MouthLampMode
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, shutdown, test_start_run_program
from test.test_connect import test_get_device_by_name


# Test , let the eyes show an expression
async def test_play_expression():
    """Test playing emoji

     Let the robot play a built-in emoticon named "codemao1" and wait for the reply result

     #PlayExpressionResponse.isSuccess: Is it successful

     #PlayExpressionResponse.resultCode: Return code

    """
    block: PlayExpression = PlayExpression(express_name="codemao1")
    # response: PlayExpressionResponse
    (resultType, response) = await block.execute()

    print(f'test_play_expression result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_play_expression timetout'
    assert response is not None and isinstance(response,
                                               PlayExpressionResponse), 'test_play_expression result unavailable'
    assert response.isSuccess, 'play_expression failed'


# Test, let the robot dance/stop dancing
async def test_control_behavior():
    """Test control performance

     Let the robot start a dance named "dance_0004" and wait for the response result

    """
    # control_type: START, STOP
    block: StartBehavior = StartBehavior(name="dance_0004en")
    # response ControlBehaviorResponse
    (resultType, response) = await block.execute()

    print(f'test_control_behavior result: {response}')
    print(
        'resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_express_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_control_behavior timetout'
    assert response is not None and isinstance(response,
                                               ControlBehaviorResponse), 'test_control_behavior result unavailable'
    assert response.isSuccess, 'control_behavior failed'


async def test_stop_behavior():
    # Start
    block: StartBehavior = StartBehavior(name="dance_0004en")
    # response ControlBehaviorResponse
    asyncio.create_task(await block.execute())

    # Stop after 5 seconds
    await asyncio.sleep(5)
    block: StopBehavior = StopBehavior()
    (resultType, response) = await block.execute()
    print(f'test_stop_behavior result: {response}')


# Test, set the color of the mouth light to green and always on
async def test_set_mouth_lamp():
    # mode: mouth light mode, 0: normal mode, 1: breathing mode

    # color: mouth light color, 1: red, 2: green, 3: blue

    # duration: duration, in milliseconds, -1 means always on

    # breath_duration: The duration of one blink, in milliseconds

    """Test setting mouth light

    Set the robot's mouth light to normal mode, green and always on for 3s, and wait for the reply result

    When mode=NORMAL, the duration parameter works, indicating how long it will stay on

    When mode=BREATH, the breath_duration parameter works, indicating how often to breathe

    #SetMouthLampResponse.isSuccess: Is it successful

    #SetMouthLampResponse.resultCode: Return code

    """

    block: SetMouthLamp = SetMouthLamp(color=MouthLampColor.GREEN, mode=MouthLampMode.NORMAL,
                                       duration=3000, breath_duration=1000)
    # response:SetMouthLampResponse
    (resultType, response) = await block.execute()

    print(f'test_set_mouth_lamp result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_set_mouth_lamp timetout'
    assert response is not None and isinstance(response, SetMouthLampResponse), 'test_set_mouth_lamp result unavailable'
    assert response.isSuccess or response.resultCode == 504, 'set_mouth_lamp failed'


# Test, switch the mouth light
async def test_control_mouth_lamp():
    """Test control mouth light

     Let the robot’s mouth light turn off and wait for the result

     #ControlMouthResponse.isSuccess: Is it successful

     #ControlMouthResponse.resultCode: Return code

    """
    # is_open: True,False
    # response :ControlMouthResponse
    (resultType, response) = await ControlMouthLamp(is_open=False).execute()

    print(f'test_control_mouth_lamp result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_control_mouth_lamp timetout'
    assert response is not None and isinstance(response,
                                               ControlMouthResponse), 'test_control_mouth_lamp result unavailable'
    assert response.isSuccess or response.resultCode == 504, 'control_mouth_lamp failed'


async def main():
    device: WiFiDevice = await test_get_device_by_name()
    if device:
        await test_connect(device)
        await test_start_run_program()
        await test_play_expression()
        await test_set_mouth_lamp()
        await test_control_mouth_lamp()
        await test_control_behavior()
        await shutdown()


if __name__ == '__main__':
    asyncio.run(main())
