# noqa: INP001
import importlib
import sys
from contextlib import ContextDecorator


class ZipContext(ContextDecorator):
    def __init__(self, mod_name, params, path):
        super().__init__()
        self.mod_name = mod_name
        self.params = params.copy()
        self.path = path

    def run(self):
        sys.path.insert(0, self.path)
        import ansiblecall

        importlib.reload(ansiblecall)
        self.clean_params()
        return ansiblecall.module(self.mod_name, **self.params)

    def __enter__(self):
        self.__path = sys.path
        return self

    def __exit__(self, *exc):
        sys.path = self.__path

    def clean_params(self):
        for p in [
            "__pub_pid",
            "__pub_arg",
            "__pub_fun",
            "__pub_jid",
            "__pub_ret",
            "__pub_tgt",
            "__pub_tgt_type",
            "__pub_user",
        ]:
            if p in self.params:
                self.params.pop(p)


def run(mod_name, path, params):
    with ZipContext(mod_name=mod_name, params=params, path=path) as ctx:
        return ctx.run()
