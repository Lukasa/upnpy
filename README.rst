UPnPy: A UPnP client library for Python
=======================================

This is absolutely a work in progress.

The end goal is that this library should make it possible to easily interact
with UPnP devices on a LAN. This library should implement some significant
subset of the functionality required for a UPnP control point.

Right now it doesn't implement anything, though.

Usage
-----

.. code-block:: python

    import upnpy
    cp = upnpy.ControlPoint()
    devices = cp.discover(30)

Caveats
-------

There are some awkward requirements of asynchronicity here. For the moment most
of the API calls block for some amount of time while they listen for responses.
This is clearly less than ideal, but we'll just have to live with it for a
while.
