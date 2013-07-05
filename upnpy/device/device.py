# -*- coding: utf-8 -*-
"""
device.py
~~~~~~~~~

Defines the structure for generic UPnP devices. This can be viewed as a form of
"base device" against which all other UPnP devices are implemented.

A "device" is a slightly abstract notion in UPnP, and does not directly
correspond to a network element. Any given network element may actually be
multiple UPnP devices, or may be only a single UPnP device.
"""
import requests


class Device(object):
    """
    The base class for all UPnP devices. This class defines the expected
    interactions for all UPnP device classes. Additionally, when there is no
    suitable more-specific class that applies for a specific UPnP device, this
    class will be used to represent it.
    """
    def __init__(self):
        #: The server string, as reported by the UPnP device during discovery.
        self.server = ''

        #: The Unique Service Name for this service.
        self.service_name = ''

        #: The Search Target for the device.
        self.search_target = ''

        # The URL for the UPnP description of the device.
        self.location = ''

        #: The IP address of the device.
        self.source_ip = ''

        #: The port the device has bound.
        self.source_port = None

        #: The device's parent device (if any).
        self.parent = None

    def describe(self):
        """
        Retrieve the device description. In this case, for an unknown device,
        we just return the XML.
        """
        desc = requests.get(self.location)
        desc.raise_for_status()
        return desc.text

    def describe_from_xml_node(self, node, parent):
        """
        Describe the device from the XML node representing it in some parent
        device's XML description.

        :param node: The ElementTree node representing the root of the device.
        :param parent: (optional) The parent of this device.
        """
        pass
