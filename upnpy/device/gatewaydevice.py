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


class GatewayDeviceV1(Device):
    """
    An Internet Gateway Device V1.
    """
    def describe(self):
        """
        Retrieve the device description and use it to populate the device
        object.
        """
        r = requests.get(self.location)
        r.raise_for_status()
        root = ElementTree.fromstring(r.text)

        # Start by populating the base URL.
        self._set_base_url(root)

        self._describe_device(root)

        return

    def _set_base_url(self, root):
        """
        Given an ElementTree root of the description XML, set the base URL.

        :param root: The ElementTree root of the description XML.
        """
        base = root.find('URLBase')

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
        dev = root.find('device')

        if not dev:
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
                setattr(self, attr_name, dev.find(field).text)
            except AttributeError:
                # dev.find() returned None
                pass

        return
