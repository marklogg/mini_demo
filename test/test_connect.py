import asyncio
import logging

import mini.mini_sdk as MiniSdk
from mini.dns.dns_browser import WiFiDevice


# To search for the robot with the specified serial number (behind the robot's butt), you can enter only the tail characters of the serial number, any length, it is recommended that more than 5 characters can be matched accurately, and the timeout is 10 seconds
# The search result WiFiDevice, contains robot name, ip, port and other information
async def test_get_device_by_name():
    """Search for devices based on the suffix of the robot serial number

     To search for the robot with the specified serial number (behind the robot's butt), you can enter only the tail characters of the serial number, any length, it is recommended that more than 5 characters can be matched accurately, and a timeout of 10 seconds


     Returns:
         WiFiDevice: Contains information such as robot name, ip, port, etc.
    """
    result: WiFiDevice = await MiniSdk.get_device_by_name("00879", 10)
    print(f"test_get_device_by_name result:{result}")
    return result


# Search for the robot with the specified serial number (behind the robot butt),
async def test_get_device_list():
    """Search all devices

     Search all devices, return results after 10s

     Returns:
         [WiFiDevice]: All searched devices, WiFiDevice array

    """
    results = await MiniSdk.get_device_list(10)
    print(f"test_get_device_list results = {results}")
    return results


# The return value of MiniSdk.connect is bool, the return value is ignored here
async def test_connect(dev: WiFiDevice) -> bool:
    """Connect the device

     Connect the specified device

     Args:
         dev (WiFiDevice): The specified device object WiFiDevice

     Returns:
         bool: Whether the connection is successful

    """
    return await MiniSdk.connect(dev)


# Enter the programming mode, the robot has a tts broadcast, here through asyncio.sleep, let the current coroutine wait 6 seconds to return, let the robot finish the broadcast
async def test_start_run_program():
    """Enter programming mode demo

     Make the robot enter the programming mode, wait for the reply result, and delay 6 seconds, let the robot finish "Enter programming mode"

     Returns:
         None:

    """
    await MiniSdk.enter_program()


# Disconnect and release resources
async def shutdown():
    """Disconnect and release resources

     Disconnect the currently connected device and release resources

    """
    await MiniSdk.quit_program()
    await MiniSdk.release()


# The default log level is Warning, set to INFO
MiniSdk.set_log_level(logging.INFO)
# Set robot type
MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)


async def main():
    device: WiFiDevice = await test_get_device_by_name()
    if device:
        await test_connect(device)
        await shutdown()


if __name__ == '__main__':
    asyncio.run(main())
