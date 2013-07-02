# -*- coding: utf-8 -*-
"""
upnpy.device
~~~~~~~~~~~~

This module contains classes that define behaviours of UPnP devices.
"""
from .device import Device, device_from_httpu_response, device_map
from .gatewaydevice import GatewayDeviceV1

#: The device map maps Search Target strings
#: (e.g. 'urn:schemas-upnp-org:service:Layer3Forwarding:1') to the classes
#: that should be used for those devices. If a search target string cannot be
#: found, the generic Device class will be used.
device_map = {
    'urn:schemas-upnp-org:device:InternetGatewayDevice:1': GatewayDeviceV1
}
