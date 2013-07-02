# -*- coding: utf-8 -*-
"""
service.py
~~~~~~~~~~

Define a base Service class. This is the class that is used when we don't know
anything about a given Service.
"""

class Service(object):
    """
    The base class for all UPnP services. This defines the minimum interface
    required for all services, and provides a representation for services that
    are unknown to UPnPy.
    """
    def __init__(self):
        #: The UPnP type of the service, e.g.
        #: "urn:schemas-upnp-org:service:Layer3Forwarding:1".
        self.service_type = ''

        #: The identifier for the service, e.g.
        #: "urn:upnp.org:serviceId:L3Forwarding1"
        self.service_id = ''

        #: The URL to the service description.
        self.scpdurl = ''

        #: The URL for control.
        self.control_url = ''

        #: The URL for subscribing to events.
        self.event_sub_url = ''
