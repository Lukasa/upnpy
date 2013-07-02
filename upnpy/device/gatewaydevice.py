# -*- coding: utf-8 -*-
"""
gatewaydevice.py
~~~~~~~~~~~~~~~~

This is an implementation of the Internet Gateway Device v1.0 specification.
It explicitly knows how to parse the XML device description for IGDs.
"""
import requests
import xml.etree.ElementTree
from .device import Device


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
        xml = ElementTree.parse(r.text).getroot()

        # Begin by setting the base URL.
        return xml

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
