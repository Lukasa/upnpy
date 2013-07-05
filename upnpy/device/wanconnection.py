# -*- coding: utf-8 -*-
"""
wanconnection.py
~~~~~~~~~~~~~~~~

The object representing the UPnP WANConnectionDevice V1.
"""
from .device import Device
from ..utils import camelcase_to_underscore


class WANConnectionV1(Device):
    """
    An implementation of the UPnP WANConnectionDevice V1 specification. This
    device enables a UPnP Control Point to configure and control IP connections
    on the WAN interface of a UPnP compliant InternetGatewayDevice.
    """
    def describe_from_xml_node(self, node, parent, namespace):
        """
        Uses the XML returned by the IGD description to prepare this device.

        :param node: The ElementTree node that forms the root of the device
                     description.
        :param parent: The parent of this device.
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

        for service in service_list:
            service_type = service.find(namespace + 'serviceType').text
            new_service = init_service(self, service, service_type, namespace)
            self.services.append(new_service)

        return
