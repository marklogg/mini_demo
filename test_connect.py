import asyncio
import logging

import mini.mini_sdk as MiniSdk
from mini.blockapi.block_setup import StartRunProgram
from mini.dns.dns_browser import WiFiDevice


# 搜索指定序列号(在机器人屁股后面)的机器人, 10秒超时
# 搜索的结果WiFiDevice, 包含机器人名称,ip,port等信息
async def test_get_device_by_name():
    result: WiFiDevice = await MiniSdk.get_device_by_name("00018", 10)
    print(f"test_get_device_by_name result:{result}")
    return result


# 搜索指定序列号(在机器人屁股后面)的机器人,
async def test_get_device_list():
    results = await MiniSdk.get_device_list(10)
    print(f"test_get_device_list results = {results}")
    return results


# MiniSdk.connect 返回值为bool, 这里忽略返回值
async def test_connect(dev: WiFiDevice):
    await MiniSdk.connect(dev)


# 进入编程模式,机器人有个tts播报,这里通过asyncio.sleep 让当前协程等6秒返回,让机器人播完
async def test_start_run_program():
    await StartRunProgram().execute()
    await asyncio.sleep(6)


# 断开连接并释放资源
async def shutdown():
    await asyncio.sleep(1)
    await MiniSdk.release()


# 默认的日志级别是Warning, 设置为INFO
MiniSdk.set_log_level(logging.INFO)

if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(shutdown())
