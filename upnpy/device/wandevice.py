# -*- coding: utf-8 -*-
"""
wandevice.py
~~~~~~~~~~~~

Contains information about the global WAN device.
"""
from .device import Device
from .wanconnection import WANConnectionV1


class WANDeviceV1(Device):
    """
    A single WAN device.
    """
    def __init__(self):
        super(WANDeviceV1, self).__init__()

        self.sub_device_map = {
            'urn:schemas-upnp-org:device:WANConnectionDevice:1': WANConnectionV1,
        }
