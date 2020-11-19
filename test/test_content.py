# import asyncio
#
# from mini import mini_sdk as MiniSdk
# from mini.apis.api_content import LanType
# from mini.apis.api_content import QueryWiKi, WikiResponse
# from mini.apis.api_content import StartTranslate, TranslateResponse
# from mini.apis.base_api import MiniApiResultType
# from mini.dns.dns_browser import WiFiDevice
# from test.test_connect import test_get_device_by_name
#
#
# # Test, check wiki
# async def test_query_wiki():
#     """Query encyclopedia demo
#
#      Query encyclopedia, query content "excellent must choose", and wait for the result, the robot broadcasts the query result
#
#      #WikiResponse.isSuccess: Is it successful
#
#      #WikiResponse.resultCode: Return code
#
#     """
#     # query:查询关键字
#     block: QueryWiKi = QueryWiKi(query='优必选')
#     # response : WikiResponse
#     (resultType, response) = await block.execute()
#
#     print(f'test_query_wiki result: {response}')
#
#     assert resultType == MiniApiResultType.Success, 'test_query_wiki timetout'
#     assert response is not None and isinstance(response, WikiResponse), 'test_query_wiki result unavailable'
#     assert response.isSuccess, 'query_wiki failed'
#
#
# # Test translation interface
# async def test_start_translate():
#     """Translation demo
#
#      Use Baidu translation to translate "Zhang Xueyou" from Chinese to English, and wait for the result, the robot broadcasts the translation result
#
#      #TranslateResponse.isSuccess: Is it successful
#
#      #TranslateResponse.resultCode: Return code
#
#      # query: keywords
#
#      # from_lan: source language
#
#      # to_lan: target language
#
#      # platform: BAIDU, GOOGLE, TENCENT
#
#     """
#
#     block: StartTranslate = StartTranslate(query="张学友", from_lan=LanType.CN, to_lan=LanType.EN)
#     # response: TranslateResponse
#     (resultType, response) = await block.execute()
#
#     print(f'test_start_translate result: {response}')
#
#     assert resultType == MiniApiResultType.Success, 'test_start_translate timetout'
#     assert response is not None and isinstance(response, TranslateResponse), 'test_start_translate result unavailable'
#     assert response.isSuccess, 'start_translate failed'
#
#
# async def main():
#     device: WiFiDevice = await test_get_device_by_name()
#     if device:
#         await MiniSdk.connect(device)
#         await MiniSdk.enter_program()
#         await test_query_wiki()
#         await test_start_translate()
#         await MiniSdk.quit_program()
#         await MiniSdk.release()
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
