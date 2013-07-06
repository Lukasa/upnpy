# -*- coding: utf-8 -*-
"""
wanconnection.py
~~~~~~~~~~~~~~~~

The object representing the UPnP WANConnectionDevice V1.
"""
from .device import Device


class WANConnectionV1(Device):
    """
    An implementation of the UPnP WANConnectionDevice V1 specification. This
    device enables a UPnP Control Point to configure and control IP connections
    on the WAN interface of a UPnP compliant InternetGatewayDevice.
    """
