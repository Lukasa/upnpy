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

# Minimum and maximum ports to bind to locally.
LOW_PORT  = 10000
HIGH_PORT = 65535

# SSDP port
SSDP_PORT = 1900


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

        return self._listen_for_discover(duration)

    def _listen_for_discover(self, duration):
        """
        Listen for responses to the discovery packet for a number of seconds up
        to the value of ``duration``.

        :param duration: The number of seconds to listen for responses to the
                         initial discovery request.
        """
        start = time.time()

        while (time.time() < (start + duration)):
            try:
                data, addr = self.__udp_socket.recvfrom(2048)
                print data
            except socket.error:
                pass

        return
