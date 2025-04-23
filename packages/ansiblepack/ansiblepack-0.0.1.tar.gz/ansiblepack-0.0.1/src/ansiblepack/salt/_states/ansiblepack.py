# noqa: INP001


"""
Run ansible modules as state modules via a salt proxy.

.. code-block:: yaml

    my_state:
      ansiblepack.module:
        - mod_name: ansible.builtin.ping
        - params:
            data: hello

"""

import json
import logging

__proxyenabled__ = ["ansiblepack"]
log = logging.getLogger(__name__)


def module(name, mod_name, params):
    """
    Run ansible modules statefully.

    :param name: State Id
    :param mod_name: Name of the ansible module to be run.
    :param params: Parameters for the ansible module
    :return: A standard Salt changes dictionary
    """
    # setup return structure
    ret = {
        "name": name,
        "changes": {},
        "result": False,
        "comment": "",
    }

    if __opts__["test"]:  # noqa: F821
        params["_ansible_check_mode"] = True

    params["_ansible_diff"] = True

    mod_ret = __salt__["ansiblepack.module"](mod_name=mod_name, **params)  # noqa: F821

    failed = mod_ret.pop("failed", False)
    changed = mod_ret.pop("changed", None)
    diff = mod_ret.pop("diff", {}) if changed else {}
    if failed:
        ret["comment"] = mod_ret.pop("msg", None)
        ret["result"] = False
    elif __opts__["test"]:  # noqa: F821
        if diff:
            mod_ret["check_mode"] = True
            mod_ret["diff"] = diff
            ret["comment"] = json.dumps(mod_ret)
        else:
            ret["comment"] = "System already in the correct state."
        ret["result"] = None
    else:
        if diff:
            ret["changes"] = {"diff": diff}
        else:
            ret["comment"] = "System already in the correct state."
        ret["result"] = True

    return ret
