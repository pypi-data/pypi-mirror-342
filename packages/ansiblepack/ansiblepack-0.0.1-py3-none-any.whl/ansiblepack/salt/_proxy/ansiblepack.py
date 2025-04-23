# noqa: INP001

"""
ansiblepack
===========

Proxy minion for running ansible modules.


Pillar
------

The ansiblepack proxy configuration is below:

.. code-block:: yaml

    proxy:
      proxytype: ansiblepack

"""

import logging

__proxyenabled__ = ["ansiblepack"]
log = logging.getLogger(__name__)


def init(opts):
    """
    Perform any needed setup.
    """
    log.debug("opts: %s", opts)


def ping():
    """
    Is the ansiblepack api responding?
    """
    return True


def shutdown(opts):
    """
    For this proxy shutdown is a no-op
    """
    log.debug("ansiblepack proxy shutdown() called with opts: %s", opts)
