# -*- coding: utf-8 -*-
"""
httpu.py
~~~~~~~~

This file contains various utilities for parsing HTTPU responses. Currently
this code is very simple and likely to break if looked at the wrong way. That's
ok for now.
"""

class HTTPUResponse(object):
    """
    Representation of a single HTTPU Response. Basically a glorified
    dictionary.
    """
    def __init__(self):
        #: The numerical response code on the response.
        self.response_code = 0

        #: The reason phrase on the response.
        self.reason = None

        #: The message body.
        self.body = ''

        #: The headers on the message. Currently a case-sensitive dict.
        self.headers = {}

        #: A string containing the source IP.
        self.source_ip = ''

        #: A string containing the source port.
        self.source_port = ''

    @classmethod
    def from_datagram(cls, datagram, source_address):
        """
        Parse a UDP datagram containing an HTTPU message into a HTTPUResponse
        object. Currently this isn't super resilient, so any significant
        deviation from the spec could cause something horrible to happen here.

        :param datagram: The UDP datagram data to parse.
        :param source_address: The socket address that the packet came from.
        """
        resp = cls()

        # Begin by applying the source IP and port.
        resp.source_ip, resp.source_port = source_address

        # Get each line in the datagram.
        lines = datagram.split('\r\n')

        # Some awful implementations send blank lines at the start of the
        # packet. We don't want them.
        while (not lines[0]):
            lines.pop(0)

        # Grab the response code and the reason from the first line.
        top_line = lines.pop(0).split(' ')
        resp.response_code = int(top_line[1])
        resp.reason = top_line[2]

        # The next set of lines will be the HTTP headers. These will be
        # separated from the body by a blank line.
        while (lines[0]):
            # We pretend that header keys can't contain colons. They can, but
            # mostly they don't, so we should be fine.
            key, value = lines.pop(0).split(':', 1)
            resp.headers[key.strip()] = value.strip()

        # What remains is the HTTP body. Combine it all back up and whack it
        # in.
        resp.body = '\r\n'.join(lines[1:])

        return resp
