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
    """Test monitor speech recognition

     Monitor speech recognition events, verify whether the recognition is successful, whether the recognized result text has a value, and store the result in the result array

     Delay 5s, end the function, check whether there is a value in the result

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
    """Test the number of monitored faces

     Monitor the number of faces, verify the successful result, verify that the number of faces is greater than 0 (need to be in front of the robot), and store the result of the number of faces in the result array

     Delay 5s, end the function, check whether the result array has a value

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
    """Test monitor face recognition

     Monitor the face recognition event, verify the successful result, verify whether the recognized face information is empty (the face needs to be in front of the robot), and store the face information in the result array

     End monitoring after 10s

     Delay 5s, end the function, check whether the result array has a value

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
    """Test monitor infrared distance

     Monitor infrared distance events, verify whether the result distance is valid (distance>0), and store it in the result array

     Delay 5s, end the function, check whether the result array has a value

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
    """Test and monitor robot attitude changes

     Monitor the robot posture change (manually change the robot posture), verify whether the result status is valid (status>0), and store it in the result array

     Delay 5s, end the function, and check whether the result array has a value

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
    """Test listening for head events

     Monitor the robot head event (manually tap the robot head), verify whether the result type is valid (type>0), and store it in the result array

     Delay 5s, end the function, and check whether the result array has a value

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
