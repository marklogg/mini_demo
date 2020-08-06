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
    """执行一个动作demo

    控制机器人执行一个指定名称的本地(内置/自定义)动作，并等待执行结果回复

    动作名称可用GetActionList获取

    #PlayActionResponse.isSuccess : 是否成功

    #PlayActionResponse.resultCode : 返回码

    """
    # action_name: 动作文件名, 可以通过GetActionList获取机器人支持的动作
    block: PlayAction = PlayAction(action_name='018')
    # response: PlayActionResponse
    (resultType, response) = await block.execute()

    print(f'test_play_action result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_play_action timetout'
    assert response is not None and isinstance(response, PlayActionResponse), 'test_play_action result unavailable'
    assert response.isSuccess, 'play_action failed'


# 测试, 控制机器人,向前/后/左/右 移动
async def test_move_robot():
    """控制机器人移动demo

    控制机器人往左(LEFTWARD)移动10步，并等待执行结果

    #MoveRobotResponse.isSuccess : 是否成功　

    #MoveRobotResponse.code : 返回码

    """
    # step: 移动几步
    # direction: 方向,枚举类型
    block: MoveRobot = MoveRobot(step=10, direction=MoveRobotDirection.LEFTWARD)
    # response : MoveRobotResponse
    (resultType, response) = await block.execute()

    print(f'test_move_robot result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_move_robot timetout'
    assert response is not None and isinstance(response, MoveRobotResponse), 'test_move_robot result unavailable'
    assert response.isSuccess, 'move_robot failed'


# 测试, 获取支持的动作文件列表
async def test_get_action_list():
    """获取动作列表demo

    获取机器人内置的动作列表，等待回复结果

    """
    # action_type: INNER 是指机器人内置的不可修改的动作文件, CUSTOM 是放置在sdcard/customize/action目录下可被开发者修改的动作
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
