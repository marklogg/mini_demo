import asyncio

from mini.apis.api_behavior import StartBehavior
from mini.apis.api_observe import ObserveHeadRacket, HeadRacketType
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_observeheadracket_pb2 import ObserveHeadRacketResponse
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


# 测试, 触摸监听
async def test_ObserveHeadRacket():
    """监听拍头事件demo

    监听拍头事件，当机器人头部被拍击时，上报拍头类型

    当机器人头部被双击时，停止监听，并跳一个舞蹈

    # ObserveHeadRacketResponse.type:

    # class HeadRacketType(enum.Enum):

    #     SINGLE_CLICK = 1  # 单击

    #     LONG_PRESS = 2  # 长按

    #     DOUBLE_CLICK = 3  # 双击

    """
    # 创建监听
    observer: ObserveHeadRacket = ObserveHeadRacket()

    # 事件处理器
    # ObserveHeadRacketResponse.type:
    # @enum.unique
    # class HeadRacketType(enum.Enum):
    #     SINGLE_CLICK = 1  # 单击
    #     LONG_PRESS = 2  # 长按
    #     DOUBLE_CLICK = 3  # 双击
    def handler(msg: ObserveHeadRacketResponse):
        # 监听到一个事件后,停止监听,
        print("{0}".format(str(msg.type)))

        if msg.type == HeadRacketType.DOUBLE_CLICK.value:
            observer.stop()
            # 执行个舞动
            asyncio.create_task(__dance())

    observer.set_handler(handler)
    # 启动
    observer.start()
    await asyncio.sleep(0)


async def __dance():
    await StartBehavior(name="dance_0002").execute()
    # 结束event_loop
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveHeadRacket())
        # 定义了事件监听对象,必须让event_loop.run_forver()
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
