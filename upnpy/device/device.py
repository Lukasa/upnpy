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
from ..utils import camelcase_to_underscore
from ..service import init_service


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

        #: A mapping of UPnP service type strings to subdevices of this device.
        self.sub_device_map = {}

        #: Any services implemented by this UPnP device.
        self.services = []

        #: Any sub-devices of this UPnP device.
        self.devices = []

    def describe(self):
        """
        Retrieve the device description. In this case, for an unknown device,
        we just return the XML.
        """
        desc = requests.get(self.location)
        desc.raise_for_status()
        return desc.text

    def describe_from_xml_node(self, node, parent, namespace):
        """
        Describe the device from the XML node representing it in some parent
        device's XML description.

        :param node: The ElementTree node representing the root of the device.
        :param parent: (optional) The parent of this device.
        :param namespace: The ElementTree namespace used in the XML.
        """
        self.parent = parent

        # Try to get the base URL, and if not available use the parent's.
        try:
            self.base_url = node.find(namespace + 'URLBase').text
        except AttributeError:
            self.base_url = parent.base_url

        # Populate some of the informational fields. These are all plain
        # strings.
        informational_fields = ['deviceType', 'friendlyName', 'manufacturer',
                                'manufacturerURL', 'modelDescription',
                                'modelName', 'modelNumber', 'modelURL',
                                'serialNumber', 'UDN', 'UPC',
                                'presentationURL']

        for field in informational_fields:
            try:
                attr_name = camelcase_to_underscore(field)
                setattr(self, attr_name, node.find(namespace + field).text)
            except AttributeError:
                pass

        # Create child services. No, not that kind.
        service_list = node.find(namespace + 'serviceList')
        service_list = service_list if service_list is not None else []

        for service in service_list:
            service_type = service.find(namespace + 'serviceType').text
            new_service = init_service(self, service, service_type, namespace)
            self.services.append(new_service)

        # Create child devices.
        device_list = node.find(namespace + 'deviceList')
        device_list = device_list if device_list is not None else []

        for device in device_list:
            device_type = device.find(namespace + 'deviceType').text
            new_device = self.sub_device_map.get(device_type, Device)()
            new_device.server = self.server
            new_device.source_ip = self.source_ip
            new_device.source_port = self.source_port
            new_device.describe_from_xml_node(device, self, namespace)
            self.devices.append(new_device)

        return
