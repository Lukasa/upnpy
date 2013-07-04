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

    :param parent: The parent device that implements this service.
    :param service_root: The ElementTree root element of the XML describing the
                         service.
    :param service_type: The UPnP string defining this service type.
    :param namespace: The namespace that ElementTree annoying applies to all
                      its XML tags.
    """
    def __init__(self, parent, service_root, service_type, namespace):
        #: The UPnP type of the service, e.g.
        #: "urn:schemas-upnp-org:service:Layer3Forwarding:1".
        self.service_type = service_type

        #: The identifier for the service, e.g.
        #: "urn:upnp.org:serviceId:L3Forwarding1"
        self.service_id = service_root.find(namespace + 'serviceId').text

        #: The URL to the service description.
        self.scpdurl = service_root.find(namespace + 'SCPDURL').text

        #: The URL for control.
        self.control_url = service_root.find(namespace + 'controlURL').text

        #: The URL for subscribing to events.
        self.event_sub_url = service_root.find(namespace + 'eventSubURL').text
