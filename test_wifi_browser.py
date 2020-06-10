#!/usr/bin/env python3

import asyncio

from mini.dns.dns_browser import WiFiDeviceListener, WiFiDevice


class MyDeviceListener(WiFiDeviceListener):

    def on_device_updated(self, device: WiFiDevice) -> None:
        pass

    def on_device_removed(self, device: WiFiDevice) -> None:
        pass

    def on_device_found(self, device: WiFiDevice):
        print(self, "onDeviceFound:", device)


listener = MyDeviceListener()

listener2 = MyDeviceListener()

from mini.channels.websocket_client import ubt_websocket as SocketClient

print(f'{SocketClient()}')

from mini.dns.dns_browser import browser


async def test_browser():
    browser().add_listener(listener)
    browser().add_listener(listener2)
    browser().remove_listener(None)
    browser().remove_all_listener()
    browser().start_scan(10000)
    await asyncio.sleep(10)
    try:
        input("Press enter to exit...\n\n")
    finally:
        browser().stop_scan()
        exit()


asyncio.get_event_loop().run_until_complete(test_browser())
