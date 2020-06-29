import asyncio

from mini.apis.api_content import QueryWiKi, WikiResponse
from mini.apis.api_content import StartTranslate, TranslateResponse
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.cloudtranslate_pb2 import CN, EN
from test.test_connect import test_connect, shutdown, test_start_run_program
from test.test_connect import test_get_device_by_name


# 测试, 查询wiki
async def test_query_wiki():
    """查询百科demo

    查询百科，查询内容"优必选"，并等待结果，机器人播报查询结果

    #WikiResponse.isSuccess : 是否成功

    #WikiResponse.resultCode : 返回码

    """
    # query:查询关键字
    block: QueryWiKi = QueryWiKi(query='优必选')
    # response : WikiResponse
    (resultType, response) = await block.execute()

    print(f'test_query_wiki result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_query_wiki timetout'
    assert response is not None and isinstance(response, WikiResponse), 'test_query_wiki result unavailable'
    assert response.isSuccess, 'query_wiki failed'


# 测试翻译接口
async def test_start_translate():
    """翻译demo

    使用百度翻译，把"张学友"，从中文翻译成英文，并等待结果，机器人播报翻译结果

    #TranslateResponse.isSuccess : 是否成功

    #TranslateResponse.resultCode : 返回码

    # query: 关键字

    # from_lan: 源语言

    # to_lan: 目标语言
    
    # platform: BAIDU, GOOGLE, TENCENT

    """

    block: StartTranslate = StartTranslate(query="张学友", from_lan=CN, to_lan=EN)
    # response: TranslateResponse
    (resultType, response) = await block.execute()

    print(f'test_start_translate result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_start_translate timetout'
    assert response is not None and isinstance(response, TranslateResponse), 'test_start_translate result unavailable'
    assert response.isSuccess, 'start_translate failed'


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_query_wiki())
        asyncio.get_event_loop().run_until_complete(test_start_translate())
        asyncio.get_event_loop().run_until_complete(shutdown())
