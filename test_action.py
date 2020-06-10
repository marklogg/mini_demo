import asyncio

from mini.blockapi.base_api import BlockApiResultType
from mini.blockapi.block_action import ChangeRobotVolume, ChangeRobotVolumeResponse
from mini.blockapi.block_action import GetActionList, GetActionListResponse, RobotActionType
from mini.blockapi.block_action import MoveRobot, MoveRobotDirection, MoveRobotResponse
from mini.blockapi.block_action import PlayAction, PlayActionResponse
from mini.dns.dns_browser import WiFiDevice
from .test_connect import test_connect, shutdown
from .test_connect import test_get_device_by_name, test_start_run_program


# 测试, 执行一个动作文件
async def test_play_action():
    # action_name: 动作文件名, 可以通过GetActionList获取机器人支持的动作
    block: PlayAction = PlayAction(action_name='018')
    # response: PlayActionResponse
    (resultType, response) = await block.execute()

    print(f'test_play_action result:{response}')

    assert resultType == BlockApiResultType.Success, 'test_play_action timetout'
    assert response is not None and isinstance(response, PlayActionResponse), 'test_play_action result unavailable'
    assert response.isSuccess, 'play_action failed'


# 测试, 控制机器人,向前/后/左/右 移动
async def test_move_robot():
    # step: 移动几步
    # direction: 方向,枚举类型
    block: MoveRobot = MoveRobot(step=10, direction=MoveRobotDirection.LEFTWARD)
    # response : MoveRobotResponse
    (resultType, response) = await block.execute()

    print(f'test_move_robot result:{response}')

    assert resultType == BlockApiResultType.Success, 'test_move_robot timetout'
    assert response is not None and isinstance(response, MoveRobotResponse), 'test_move_robot result unavailable'
    assert response.isSuccess, 'move_robot failed'


# 测试, 获取支持的动作文件列表
async def test_get_action_list():
    # action_type: INNER 是指机器人内置的不可修改的动作文件, CUSTOM 是放置在sdcard/customize/action目录下可被开发者修改的动作
    block: GetActionList = GetActionList(action_type=RobotActionType.INNER)
    # response:GetActionListResponse
    (resultType, response) = await block.execute()

    print(f'test_get_action_list result:{response}')

    assert resultType == BlockApiResultType.Success, 'test_get_action_list timetout'
    assert response is not None and isinstance(response,
                                               GetActionListResponse), 'test_get_action_list result unavailable'
    assert response.isSuccess, 'get_action_list failed'


# 测试, 改变机器人的音量
async def test_change_robot_volume():
    # volume: 0~1.0
    block: ChangeRobotVolume = ChangeRobotVolume(volume=0.5)
    # response:ChangeRobotVolumeResponse
    (resultType, response) = await block.execute()

    print(f'test_change_robot_volume result:{response}')

    assert resultType == BlockApiResultType.Success, 'test_change_robot_volume timetout'
    assert response is not None and isinstance(response,
                                               ChangeRobotVolumeResponse), 'test_change_robot_volume result unavailable'
    assert response.isSuccess, 'get_action_list failed'


async def main():
    device: WiFiDevice = await test_get_device_by_name()
    if device:
        await test_connect(device)
        await test_start_run_program()
        await test_play_action()
        await test_move_robot()
        await test_get_action_list()
        await test_change_robot_volume()
        await shutdown()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
