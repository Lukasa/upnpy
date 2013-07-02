# -*- coding: utf-8 -*-
"""
upnpy.service
~~~~~~~~~~~~~

This submodule defines services and their interactions.
"""
from .service import Service


service_map = {}


def init_service(parent_device, service_root, service_type):
    """
    Given the root element of the service and the parent device, create the
    most appropriate service.

    :param parent_device: The parent device hosting the service.
    :param service_root: The ElementTree root element of the service XML.
    :param service_type: The UPnP service type string identifying the service.
    """
    try:
        service = service_map[service_type]()
    except KeyError:
        service = Service()

    return service
