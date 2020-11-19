import asyncio
import logging

import mini.mini_sdk as MiniSdk
from mini.dns.dns_browser import WiFiDevice


# 搜索指定序列号(在机器人屁股后面)的机器人, 可以只输入序列号尾部字符即可,长度任意, 建议5个字符以上可以准确匹配, 10秒超时
# 搜索的结果WiFiDevice, 包含机器人名称,ip,port等信息
async def test_get_device_by_name():
    """根据机器人序列号后缀搜索设备

    搜索指定序列号(在机器人屁股后面)的机器人, 可以只输入序列号尾部字符即可,长度任意, 建议5个字符以上可以准确匹配, 10秒超时


    Returns:
        WiFiDevice: 包含机器人名称,ip,port等信息

    """
    result: WiFiDevice = await MiniSdk.get_device_by_name("00879", 10)
    print(f"test_get_device_by_name result:{result}")
    return result


# 搜索指定序列号(在机器人屁股后面)的机器人,
async def test_get_device_list():
    """搜索所有设备

    搜索所有设备，10s后返回结果

    Returns:
        [WiFiDevice]: 所有搜索到的设备，WiFiDevice数组

    """
    results = await MiniSdk.get_device_list(10)
    print(f"test_get_device_list results = {results}")
    return results


# MiniSdk.connect 返回值为bool, 这里忽略返回值
async def test_connect(dev: WiFiDevice) -> bool:
    """连接设备

    连接指定的设备

    Args:
        dev (WiFiDevice): 指定的设备对象 WiFiDevice

    Returns:
        bool: 是否连接成功

    """
    return await MiniSdk.connect(dev)


# 进入编程模式,机器人有个tts播报,这里通过asyncio.sleep 让当前协程等6秒返回,让机器人播完
async def test_start_run_program():
    """进入编程模式demo

    使机器人进入编程模式，等待回复结果，并延时6秒，让机器人播完"进入编程模式"

    Returns:
        None:

    """
    await MiniSdk.enter_program()


# 断开连接并释放资源
async def shutdown():
    """断开连接并释放资源

    断开当前连接的设备，并释放资源

    """
    await MiniSdk.quit_program()
    await MiniSdk.release()


# 默认的日志级别是Warning, 设置为INFO
MiniSdk.set_log_level(logging.INFO)
# 设置机器人类型
MiniSdk.set_robot_type(MiniSdk.RobotType.DEDU)


async def main():
    device: WiFiDevice = await test_get_device_by_name()
    if device:
        await test_connect(device)
        await shutdown()


if __name__ == '__main__':
    asyncio.run(main())
