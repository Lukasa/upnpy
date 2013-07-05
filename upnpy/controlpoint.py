# -*- coding: utf-8 -*-
"""
controlpoint.py
~~~~~~~~~~~~~~~

This file contains the primary ControlPoint class. This is the core portion of
the API, and implements the bulk of the UPnP functionality.
"""
import socket
import random
import time
from .httpu import HTTPUResponse
from .device import Device, GatewayDeviceV1, WANConnectionV1

# Minimum and maximum ports to bind to locally.
LOW_PORT  = 10000
HIGH_PORT = 65535

# SSDP port
SSDP_PORT = 1900

#: The device map maps Search Target strings
#: (e.g. 'urn:schemas-upnp-org:service:Layer3Forwarding:1') to the classes
#: that should be used for those devices. If a search target string cannot be
#: found, the generic Device class will be used.
device_map = {
    'urn:schemas-upnp-org:device:InternetGatewayDevice:1': GatewayDeviceV1
}


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
    dev.source_ip = response.source_ip
    dev.source_port = response.source_port

    return dev


class ControlPoint(object):
    """
    Represents a single UPnP control point.
    """
    def __init__(self):
        self.__bind_sockets()

    def __bind_sockets(self):
        """
        Bind any necessary sockets.
        """
        local_port = random.randint(LOW_PORT, HIGH_PORT)
        self.__udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__udp_socket.bind(('', local_port))
        self.__udp_socket.setblocking(0)
        return

    def discover(self, duration):
        """
        Discover UPnP devices on the network.

        :param duration: The number of seconds to listen for responses to the
                         initial discovery request.
        """
        # Set the socket to broadcast mode.
        self.__udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Build the message. Currently, this just involves blatting a
        # pre-written message over the wire.
        msg = '\r\n'.join(["M-SEARCH * HTTP/1.1",
                           "HOST: 239.255.255.250:1900",
                           "MAN: ssdp:discover",
                           "MX: " + str(duration),
                           "ST: ssdp:all",
                           ""])

        # Send the message.
        self.__udp_socket.sendto(msg, ('<broadcast>', SSDP_PORT))

        # Get the responses.
        packets = self._listen_for_discover(duration)

        # Parse them.
        packets = [HTTPUResponse.from_datagram(*packet) for packet in packets]

        # Build the devices.
        devices = [device_from_httpu_response(packet) for packet in packets]

        return devices

    def _listen_for_discover(self, duration):
        """
        Listen for responses to the discovery packet for a number of seconds up
        to the value of ``duration``.

        :param duration: The number of seconds to listen for responses to the
                         initial discovery request.
        """
        start = time.time()
        packets = []

        while (time.time() < (start + duration)):
            try:
                data, addr = self.__udp_socket.recvfrom(2048)
                packets.append((data, addr))
            except socket.error:
                pass

        return packets
