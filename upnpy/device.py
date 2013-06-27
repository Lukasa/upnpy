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


#: The device map maps Search Target strings
#: (e.g. 'urn:schemas-upnp-org:service:Layer3Forwarding:1') to the classes
#: that should be used for those devices. If a search target string cannot be
#: found, the generic Device class will be used.
device_map = {}


def device_from_httpu_response(response):
    """
    Given a single HTTPU response, prepares a basic in-memory representation of
    the device. The devices returned from this function will be very basic: in
    particular, they will not have had their descriptions retrieved yet.
    """
    st_string = response.headers['ST']

    try:
        dev = device_map[st_string]()
    except KeyError:
        dev = Device()

    dev.server = response.headers['SERVER']
    dev.service_name = response.headers['USN']
    dev.search_target = response.headers['ST']
    dev.location = response.headers['LOCATION']

    return dev


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

    def describe(self):
        """
        Retrieve the device description. In this case, for an unknown device,
        we just return the XML.
        """
        desc = requests.get(self.location)
        desc.raise_for_status()
        return desc.text
