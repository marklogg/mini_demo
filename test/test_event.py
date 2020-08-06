#!/usr/bin/env python3

import asyncio

from mini.apis.api_observe import ObserveFaceDetect, FaceDetectTaskResponse
from mini.apis.api_observe import ObserveFaceRecognise, FaceRecogniseTaskResponse
from mini.apis.api_observe import ObserveHeadRacket, ObserveHeadRacketResponse
from mini.apis.api_observe import ObserveInfraredDistance, ObserveInfraredDistanceResponse
from mini.apis.api_observe import ObserveRobotPosture, ObserveFallClimbResponse
from mini.apis.api_observe import ObserveSpeechRecognise, SpeechRecogniseResponse
from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


async def test_speech_recognise():
    """测试监听语音识别

    监听语音识别事件，校验识别是否成功，识别的结果文本是否有值，把结果存入result数组

    延时5s，结束函数，校验result中是否有值

    """
    result = []

    observer: ObserveSpeechRecognise = ObserveSpeechRecognise()

    def handler(msg):
        print(f"test_speech_recognise handle msg:{msg.text}")

        assert msg is not None and isinstance(msg, SpeechRecogniseResponse), "test_speech_recognise result not " \
                                                                             "available "
        assert msg.isSuccess, "test_speech_recognise failed"

        assert len(msg.text), "test_speech_recognise text is nothing"

        result.append(msg.text)

    observer.set_handler(handler)
    observer.start()

    await asyncio.sleep(10)

    print('---- stop ObserveSpeechRecognise')
    observer.stop()

    await asyncio.sleep(5)

    assert len(result), "test_speech_recognise result nil"


async def test_face_detect():
    """测试监听人脸个数

    监听人脸个数，校验成功结果，校验人脸个数大于0(需要有人脸在机器人面前)，把人脸个数结果存入result数组

    延时5s，结束函数，校验result数组是否有值

    """
    result = []

    observer: ObserveFaceDetect = ObserveFaceDetect()

    def handler(msg):
        print(f"test_face_detect handle msg:{msg}")

        assert msg is not None and isinstance(msg, FaceDetectTaskResponse), "test_face_detect result not " \
                                                                            "available "
        assert msg.isSuccess, "test_face_detect failed"

        assert msg.count, "test_face_detect count is 0"

        result.append(msg.count)

    observer.set_handler(handler)
    observer.start()

    await asyncio.sleep(10)

    print('---- stop ObserveFaceDetect')
    observer.stop()

    await asyncio.sleep(5)

    assert len(result), "test_face_detect result nil"


async def test_face_recognise():
    """测试监听人脸识别

    监听人脸识别事件，校验成功结果，校验识别到的人脸信息是否为空(需有人脸在机器人面前)，并把人脸信息存入result数组

    10s后结束监听

    延时5s，结束函数，校验result数组是否有值

    """
    result = []

    observer: ObserveFaceRecognise = ObserveFaceRecognise()

    def handler(msg):
        print(f"test_face_recognise handle msg:{msg}")

        assert msg is not None and isinstance(msg, FaceRecogniseTaskResponse), "test_face_recognise result not " \
                                                                               "available "
        assert msg.isSuccess, "test_face_recognise failed"

        assert msg.faceInfos is not None, "test_face_recognise faceInfos is nil"

        result.append(msg.faceInfos)

    observer.set_handler(handler)
    observer.start()

    await asyncio.sleep(10)

    print('---- stop ObserveFaceRecognise')
    observer.stop()

    await asyncio.sleep(5)

    assert len(result), "ObserveFaceRecognise result nil"


async def test_infrared_distance():
    """测试监听红外距离

    监听红外距离事件，校验结果distance是否有效(distance>0)，并存入result数组

    延时5s，结束函数，校验result数组是否有值

    Returns:

    """
    result = []

    observer: ObserveInfraredDistance = ObserveInfraredDistance()

    def handler(msg):
        print(f"test_infrared_distance handle msg:{msg}")

        assert msg is not None and isinstance(msg, ObserveInfraredDistanceResponse), "test_infrared_distance result " \
                                                                                     "not " \
                                                                                     "available "
        # assert msg.isSuccess, "test_infrared_distance failed"

        assert msg.distance is not None and msg.distance > 0, "test_infrared_distance distance unavailable"

        result.append(msg.distance)

    observer.set_handler(handler)
    observer.start()

    await asyncio.sleep(10)

    print('---- stop ObserveInfraredDistance')
    observer.stop()

    await asyncio.sleep(5)

    assert len(result), "ObserveInfraredDistance result nil"


async def test_robot_posture():
    """测试监听机器人姿态变化

    监听机器人姿态变化(需手动改变机器人姿态)，校验结果status是否有效(status>0)，并存入result数组

    延时5s，结束函数，并校验result数组是否有值

    Returns:

    """
    result = []

    observer: ObserveRobotPosture = ObserveRobotPosture()

    def handler(msg):
        print(f"test_robot_posture handle msg:{msg}")

        assert msg is not None and isinstance(msg, ObserveFallClimbResponse), "test_robot_posture result " \
                                                                              "not " \
                                                                              "available "
        # assert msg.isSuccess, "test_infrared_distance failed"

        assert msg.status is not None and msg.status > 0, "test_robot_posture status unavailable"

        result.append(msg.status)

    observer.set_handler(handler)
    observer.start()

    await asyncio.sleep(10)

    print('---- stop ObserveRobotPosture')
    observer.stop()

    await asyncio.sleep(5)

    assert len(result), "ObserveRobotPosture result nil"


async def test_head_racket():
    """测试监听拍头事件

    监听机器人拍头事件(需手动拍打机器人头部)，校验结果type是否有效(type>0)，并存入result数组

    延时5s，结束函数，并校验result数组是否有值

    Returns:

    """
    result = []

    observer: ObserveHeadRacket = ObserveHeadRacket()

    def handler(msg):
        print(f"test_head_racket handle msg:{msg}")

        assert msg is not None and isinstance(msg, ObserveHeadRacketResponse), "test_head_racket result " \
                                                                               "not " \
                                                                               "available "
        # assert msg.isSuccess, "test_infrared_distance failed"

        assert msg.type is not None and msg.type > 0, "test_head_racket type unavailable"

        result.append(msg.type)

    observer.set_handler(handler)
    observer.start()

    await asyncio.sleep(10)

    print('---- stop ObserveHeadRacket')
    observer.stop()

    await asyncio.sleep(5)

    assert len(result), "ObserveHeadRacket result nil"


async def main():
    device: WiFiDevice = await test_get_device_by_name()
    if device:
        await test_connect(device)
        await test_start_run_program()

        await test_speech_recognise()
        await test_face_detect()
        await test_face_recognise()
        await test_infrared_distance()
        await test_robot_posture()
        await test_head_racket()

        await shutdown()


if __name__ == '__main__':
    asyncio.run(main())
