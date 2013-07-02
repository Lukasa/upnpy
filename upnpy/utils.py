# -*- coding: utf-8 -*-
"""
utils.py
~~~~~~~~

Defines utility functions used by UPnPy.
"""


def camelcase_to_underscore(text):
    """
    Convert a camelCasedString to one separated_by_underscores. Treats
    neighbouring capitals as acronyms and doesn't separated them, e.g. URL does
    not become u_r_l. That would be stupid.

    :param text: The string to convert.
    """
    outstr = []

    for char in text:
        if char.is_lower():
            outstr.append(char)
        elif outstr[-1].is_lower():
            outstr.append('_')
            outstr.append(char.lower())
        else:
            outstr.append(char.lower())

    return ''.join(outstr)
