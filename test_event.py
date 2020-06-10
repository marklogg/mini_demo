#!/usr/bin/env python3

import asyncio

from mini.blockapi.block_observe import ObserveFaceDetect, FaceDetectTaskResponse
from mini.blockapi.block_observe import ObserveFaceRecognise, FaceRecogniseTaskResponse
from mini.blockapi.block_observe import ObserveHeadRacket, ObserveHeadRacketResponse
from mini.blockapi.block_observe import ObserveInfraredDistance, ObserveInfraredDistanceResponse
from mini.blockapi.block_observe import ObserveRobotPosture, ObserveFallClimbResponse
from mini.blockapi.block_observe import ObserveSpeechRecognise, SpeechRecogniseResponse
from mini.dns.dns_browser import WiFiDevice
from test_connect import test_connect, shutdown
from test_connect import test_get_device_by_name, test_start_run_program


async def test_speech_recognise():
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


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())

        asyncio.get_event_loop().run_until_complete(test_speech_recognise())
        asyncio.get_event_loop().run_until_complete(test_face_detect())
        asyncio.get_event_loop().run_until_complete(test_face_recognise())
        asyncio.get_event_loop().run_until_complete(test_infrared_distance())
        asyncio.get_event_loop().run_until_complete(test_robot_posture())
        asyncio.get_event_loop().run_until_complete(test_head_racket())

        asyncio.get_event_loop().run_until_complete(shutdown())
