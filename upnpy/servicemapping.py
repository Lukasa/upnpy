# -*- coding: utf-8 -*-
"""
servicemap.py
~~~~~~~~~~~~~

Provides mappings to get service objects from their service type strings.
"""
from .service import Service


service_map = {}


def init_service(parent_device, service_root, service_type, namespace):
    """
    Given the root element of the service and the parent device, create the
    most appropriate service.

    :param parent_device: The parent device hosting the service.
    :param service_root: The ElementTree root element of the service XML.
    :param service_type: The UPnP service type string identifying the service.
    :param namespace: The XML namespace string prepended to all ETree nodes.
    """
    try:
        service = service_map[service_type]
    except KeyError:
        service = Service

    return service(parent_device, service_root, service_type, namespace)
