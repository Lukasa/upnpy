# -*- coding: utf-8 -*-
"""
gatewaydevice.py
~~~~~~~~~~~~~~~~

This is an implementation of the Internet Gateway Device v1.0 specification.
It explicitly knows how to parse the XML device description for IGDs.
"""
import requests
import xml.etree.ElementTree as ElementTree
from .device import Device
from ..utils import camelcase_to_underscore
from ..service import init_service

# A subsidiary device map, indicating the subsidiary devices available on an
# IGD.

class GatewayDeviceV1(Device):
    """
    An Internet Gateway Device V1.
    """
    def __init__(self):
        super(GatewayDeviceV1, self).__init__()

        self.sub_device_map = {
            'urn:schemas-upnp-org:device:WANConnectionDevice:1': WANConnectionV1,
        }

    def describe(self):
        """
        Retrieve the device description and use it to populate the device
        object.
        """
        r = requests.get(self.location)
        r.raise_for_status()
        root = ElementTree.fromstring(r.text)

        # Save off the namespace, which ElementTree obnoxiously prepends to all
        # the node names.
        self.__ns = root.tag.replace('root', '')

        # Start by populating the base URL.
        self._set_base_url(root)

        self._describe_device(root)

        return

    def _set_base_url(self, root):
        """
        Given an ElementTree root of the description XML, set the base URL.

        :param root: The ElementTree root of the description XML.
        """
        base = root.find(self.__ns + 'URLBase')

        if base:
            self.base_url = base.text
        else:
            self.base_url = ('http://' + self.source_ip + ':' +
                             str(self.source_port))
        return

    def _describe_device(self, root):
        """
        Given the root of the description XML, grab the device portion and use
        it to populate this object.

        :param root: The ElementTree root of the description XML.
        """
        self.services = []
        self.devices = []

        dev = root.find(self.__ns + 'device')

        if dev is None:
            raise ValueError('Malformed XML received: absent device tag.')

        # Begin by populating some of the informational fields. These are all
        # plain strings.
        informational_fields = ['deviceType', 'friendlyName', 'manufacturer',
                                'manufacturerURL', 'modelDescription',
                                'modelName', 'modelNumber', 'modelURL',
                                'serialNumber', 'UDN', 'UPC',
                                'presentationURL']

        for field in informational_fields:
            try:
                attr_name = camelcase_to_underscore(field)
                setattr(self, attr_name, dev.find(self.__ns + field).text)
            except AttributeError:
                # dev.find() returned None
                pass

        # Now create the child services.
        service_list = dev.find(self.__ns + 'serviceList')
        service_list = service_list if service_list is not None else []

        for service in service_list:
            service_type = service.find(self.__ns + 'serviceType').text
            new_service = init_service(self, service, service_type, self.__ns)
            self.services.append(new_service)

        # Finally, find the child devices.
        device_list = dev.find(self.__ns + 'deviceList')
        device_list = device_list if device_list is not None else []

        for device in device_list:
            device_type = device.find(self.__ns + 'deviceType').text
            new_device = self.sub_device_map.get(device_type, Device)()
            new_device.server = self.server
            new_device.source_ip = self.source_ip
            new_device.source_port = self.source_port
            new_device.describe_from_xml_node(device, self, self.__ns)
            self.devices.append(new_device)

        return
