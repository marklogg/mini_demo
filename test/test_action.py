import asyncio

from mini import mini_sdk as MiniSdk
from mini.apis.api_action import GetActionList, GetActionListResponse, RobotActionType
from mini.apis.api_action import MoveRobot, MoveRobotDirection, MoveRobotResponse
from mini.apis.api_action import PlayAction, PlayActionResponse
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_get_device_by_name


# 测试, 执行一个动作文件
async def test_play_action():
    """Perform an action demo

     Control the robot to execute a local (built-in/custom) action with a specified name and wait for the execution result to reply

     Action name can be obtained with GetActionList

     #PlayActionResponse.isSuccess: Is it successful

     #PlayActionResponse.resultCode: Return code

     """
    # action_name: Action file name, you can get the actions supported by the robot through GetActionList
    block: PlayAction = PlayAction(action_name='018')
    # response: PlayActionResponse
    (resultType, response) = await block.execute()

    print(f'test_play_action result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_play_action timetout'
    assert response is not None and isinstance(response, PlayActionResponse), 'test_play_action result unavailable'
    assert response.isSuccess, 'play_action failed'


# 测试, 控制机器人,向前/后/左/右 移动
async def test_move_robot():
    """Control the robot mobile demo

     Control the robot to move 10 steps to the left (LEFTWARD) and wait for the execution result

     #MoveRobotResponse.isSuccess: Is it successful　

     #MoveRobotResponse.code: Return code

     """
    # step: Move a few steps
    # direction: direction, enumeration type
    block: MoveRobot = MoveRobot(step=10, direction=MoveRobotDirection.LEFTWARD)
    # response : MoveRobotResponse
    (resultType, response) = await block.execute()

    print(f'test_move_robot result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_move_robot timetout'
    assert response is not None and isinstance(response, MoveRobotResponse), 'test_move_robot result unavailable'
    assert response.isSuccess, 'move_robot failed'


# 测试, 获取支持的动作文件列表
async def test_get_action_list():
    """Get action list demo

     Get the list of built-in actions of the robot and wait for the reply result

    """
    # action_type: INNER refers to the unmodifiable action file built into the robot, and CUSTOM is an action that can be modified by the developer placed in the sdcard/customize/action directory
    block: GetActionList = GetActionList(action_type=RobotActionType.INNER)
    # response:GetActionListResponse
    (resultType, response) = await block.execute()

    print(f'test_get_action_list result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_get_action_list timetout'
    assert response is not None and isinstance(response,
                                               GetActionListResponse), 'test_get_action_list result unavailable'
    assert response.isSuccess, 'get_action_list failed'


async def main():
    device: WiFiDevice = await test_get_device_by_name()
    if device:
        await MiniSdk.connect(device)
        await MiniSdk.enter_program()
        await test_play_action()
        await test_move_robot()
        await test_get_action_list()
        await MiniSdk.quit_program()
        await MiniSdk.release()


if __name__ == '__main__':
    asyncio.run(main())
