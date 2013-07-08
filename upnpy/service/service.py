# -*- coding: utf-8 -*-
"""
service.py
~~~~~~~~~~

Define a base Service class. This is the class that is used when we don't know
anything about a given Service.
"""
import requests
import xml.etree.ElementTree as ET
from ..utils import get_SOAP_RPC_base


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
        #: The parent device.
        self.parent = parent

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

    def __send_RPC_command(self,
                           action_name,
                           xml_command=None,
                           soap_args=None):
        """
        Prepares and sends a SOAP RPC command. Adds the general structure
        required for the RPC command, and then sends that command to this
        device.

        Returns the Reqeusts :class:`Response <requests.Response>` object from
        the HTTP POST.

        :param action_name: The name (including version) of the action to
                            perform.
        :param xml_command: (optional) An ElementTree node representing the
                            root of the SOAP envelope body. If you don't
                            provide this, you must provide ``soap_args``.
        :param soap_args:  (optional) A dictionary of arguments to provide on
                           the RPC call. This should be used whenever you can
                           represent the arguments in this way. If this isn't
                           provided, you must provide ``xml_command``.
        """
        if (xml_command is None) and (soap_args is None):
            raise ValueError("May not provide both xml_command and soap_args")

        # Build the default headers.
        headers = {'CONTENT-TYPE': 'text/xml; charset="utf-8"',
                   'SOAPACTION': self.service_type + '#' + action_name}

        # Prepare the skeleton of the XML.
        root, body = get_SOAP_RPC_base()

        # If we got an XML tree, just append it to the body. Otherwise, if we
        # have a dictionary, generate XML from that.
        if xml_command is not None:
            body.append(xml_command)
        else:
            # Add the action-specific tag.
            append_root = ET.SubElement(body,
                                        'u:' + action_name,
                                        {'xmlns:u': self.service_type})

            # Each element in the dictionary should have a tag.
            for argname, argval in soap_args:
                elem = ET.SubElement(append_root, argname)
                elem.text = str(argval)

        # Prepare the body string.
        post_body = '<?xml version="1.0"?>'
        post_body += ET.tostring(root)

        # Now post it.
        url = self.parent.base_url + self.control_url

        return requests.post(url, headers=headers, body=post_body)
