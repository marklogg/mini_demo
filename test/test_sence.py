import asyncio

from mini.apis import errors
from mini.apis.api_sence import FaceAnalysis, FaceAnalyzeResponse
from mini.apis.api_sence import FaceDetect, FaceDetectResponse
from mini.apis.api_sence import FaceRecognise, FaceRecogniseResponse
from mini.apis.api_sence import GetInfraredDistance, GetInfraredDistanceResponse
from mini.apis.api_sence import GetRegisterFaces, GetRegisterFacesResponse
from mini.apis.api_sence import ObjectRecognise, RecogniseObjectResponse, ObjectRecogniseType
from mini.apis.api_sence import TakePicture, TakePictureResponse, TakePictureType
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, shutdown, test_start_run_program
from test.test_connect import test_get_device_by_name


# 测试人脸侦测
async def test_face_detect():
    """测试人脸个数侦测

    侦测人脸个数，10s超时，并等待回复结果

    #FaceDetectResponse.count : 人脸个数

    #FaceDetectResponse.isSuccess : 是否成功

    #FaceDetectResponse.resultCode : 返回码

    """
    # timeout: 指定侦测时长
    block: FaceDetect = FaceDetect(timeout=10)
    # response: FaceDetectResponse
    (resultType, response) = await block.execute()

    print(f'test_face_detect result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_face_detect timetout'
    assert response is not None and isinstance(response, FaceDetectResponse), 'test_face_detect result unavailable'
    assert response.isSuccess, 'face_detect failed'


# 测试人脸分析(性别)
async def test_face_analysis():
    """测试人脸分析（性别）

    侦测人脸信息(性别、年龄)，超时时间10s，并等待回复结果

    当多人存在摄像头前时，返回占画面比例最大的那个人脸信息

    返回值：示例 {"age": 24, "gender": 99, "height": 238, "width": 238}

    age: 年龄

    gender：[1, 100], 小于50为女性，大于50为男性

    height：人脸在摄像头画面中的高度

    width：人脸在摄像头画面中的宽度

    """
    block: FaceAnalysis = FaceAnalysis(timeout=10)
    # response: FaceAnalyzeResponse
    (resultType, response) = await block.execute()

    print(f'test_face_analysis result: {response}')
    print('code = {0}, error={1}'.format(response.resultCode, errors.get_vision_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_face_analysis timetout'
    assert response is not None and isinstance(response, FaceAnalyzeResponse), 'test_face_analysis result unavailable'
    assert response.isSuccess, 'face_analysis failed'


# 测试物体识别：识别花，10s超时
async def test_object_recognise_flower():
    """测试物体(花)识别

    让机器人识别花(需手动把花或花的照片放到机器人面前)，超时10s，并等待结果

    #RecogniseObjectResponse.objects : 物体名数组[str]

    #RecogniseObjectResponse.isSuccess : 是否成功

    #RecogniseObjectResponse.resultCode : 返回码

    """
    # object_type: 支持FLOWER, FRUIT, GESTURE 三类物体
    block: ObjectRecognise = ObjectRecognise(object_type=ObjectRecogniseType.FLOWER, timeout=10)
    # response : RecogniseObjectResponse
    (resultType, response) = await block.execute()

    print(f'test_object_recognise_flower result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_object_recognise_flower timetout'
    assert response is not None and isinstance(response,
                                               RecogniseObjectResponse), 'test_object_recognise_flower result unavailable'
    assert response.isSuccess, 'test_object_recognise_flower failed'


# 测试物体识别：识别水果，10s超时
async def test_object_recognise_fruit():
    """测试物体(水果)识别

    让机器人识别花(需手动把水果或水果的照片放到机器人面前)，超时10s，并等待结果

    #RecogniseObjectResponse.objects : 物体名数组[str]

    #RecogniseObjectResponse.isSuccess : 是否成功

    #RecogniseObjectResponse.resultCode : 返回码

    """
    # object_type: 支持FLOWER, FRUIT, GESTURE 三类物体
    block: ObjectRecognise = ObjectRecognise(object_type=ObjectRecogniseType.FRUIT, timeout=10)
    # response : RecogniseObjectResponse
    (resultType, response) = await block.execute()

    print(f'test_object_recognise_fruit result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_object_recognise_fruit timetout'
    assert response is not None and isinstance(response,
                                               RecogniseObjectResponse), 'test_object_recognise_fruit result unavailable'
    assert response.isSuccess, 'test_object_recognise_fruit failed'


# 测试物体识别：识别手势，10s超时
async def test_object_recognise_gesture():
    """测试物体(手势)识别

    让机器人识别花(需手动在机器人面前作出手势)，超时10s，并等待结果

    #RecogniseObjectResponse.objects : 物体名数组[str]

    #RecogniseObjectResponse.isSuccess : 是否成功

    #RecogniseObjectResponse.resultCode : 返回码

    """
    # object_type: 支持FLOWER, FRUIT, GESTURE 三类物体
    block: ObjectRecognise = ObjectRecognise(object_type=ObjectRecogniseType.GESTURE, timeout=10)
    # response : RecogniseObjectResponse
    (resultType, response) = await block.execute()

    print(f'test_object_recognise_gesture result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_object_recognise_gesture timetout'
    assert response is not None and isinstance(response,
                                               RecogniseObjectResponse), 'test_object_recognise_gesture result unavailable'
    assert response.isSuccess, 'test_object_recognise_gesture failed'


# 测试拍照
async def test_take_picture():
    """测试拍照

    让机器人立即拍照，并等待结果

    #TakePictureResponse.isSuccess : 是否成功

    #TakePictureResponse.code : 返回码

    #TakePictureResponse.picPath : 照片在机器人里的存储路径

    """
    # response: TakePictureResponse
    # take_picture_type: IMMEDIATELY-立即拍照, FINDFACE-找到人脸再拍照 两种拍照效果
    (resultType, response) = await TakePicture(take_picture_type=TakePictureType.IMMEDIATELY).execute()

    print(f'test_take_picture result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_take_picture timetout'
    assert response is not None and isinstance(response, TakePictureResponse), 'test_take_picture result unavailable'
    assert response.isSuccess, 'test_take_picture failed'


# 测试人脸识别
async def test_face_recognise():
    """测试人脸识别

    让机器人进行人脸识别检测，超时10s，并等待结果


    #FaceRecogniseResponse.faceInfos : [FaceInfoResponse] 人脸信息数组

        FaceInfoResponse.id : 人脸id

        FaceInfoResponse.name : 姓名，如果是陌生人，则默认name为"stranger"

        FaceInfoResponse.gender : 性别

        FaceInfoResponse.age : 年龄

    #FaceRecogniseResponse.isSuccess : 是否成功

    #FaceRecogniseResponse.resultCode : 返回码

    Returns:

    """
    # response : FaceRecogniseResponse
    (resultType, response) = await FaceRecognise(timeout=10).execute()

    print(f'test_face_recognise result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_face_recognise timetout'
    assert response is not None and isinstance(response,
                                               FaceRecogniseResponse), 'test_face_recognise result unavailable'
    assert response.isSuccess, 'test_face_recognise failed'


# 测试获取红外探测距离
async def test_get_infrared_distance():
    """测试红外距离检测

    获取当前机器人检测到的红外距离，并等待结果

    #GetInfraredDistanceResponse.distance : 红外距离

    """
    # response: GetInfraredDistanceResponse
    (resultType, response) = await GetInfraredDistance().execute()

    print(f'test_get_infrared_distance result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_get_infrared_distance timetout'
    assert response is not None and isinstance(response,
                                               GetInfraredDistanceResponse), 'test_get_infrared_distance result unavailable'
    assert response.distance > 0, 'test_get_infrared_distance failed'


# 测试获取目前机器人内注册的人脸个数
async def test_get_register_faces():
    """测试获取已注册的人脸信息

    获取在机器人中已注册的所有人脸信息，并等待结果

    #GetRegisterFacesResponse.faceInfos : [FaceInfoResponse] 人脸信息数组

        #FaceInfoResponse.id : 人脸id

        #FaceInfoResponse.name : 姓名

        #FaceInfoResponse.gender : 性别

        #FaceInfoResponse.age : 年龄

    #GetRegisterFacesResponse.isSuccess : 是否成功

    #GetRegisterFacesResponse.resultCode : 返回码

    Returns:

    """
    # reponse : GetRegisterFacesResponse
    (resultType, response) = await GetRegisterFaces().execute()

    print(f'test_get_register_faces result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_get_register_faces timetout'
    assert response is not None and isinstance(response,
                                               GetRegisterFacesResponse), 'test_get_register_faces result unavailable'
    assert response.isSuccess, 'test_get_register_faces failed'


async def main():
    device: WiFiDevice = await test_get_device_by_name()
    if device:
        await test_connect(device)
        await test_start_run_program()

        await test_face_detect()
        await test_face_analysis()
        await test_take_picture()
        await test_face_recognise()
        await test_get_infrared_distance()
        await test_get_register_faces()
        await test_object_recognise_flower()
        await test_object_recognise_fruit()
        await test_object_recognise_gesture()

        await shutdown()


if __name__ == '__main__':
    asyncio.run(main())
