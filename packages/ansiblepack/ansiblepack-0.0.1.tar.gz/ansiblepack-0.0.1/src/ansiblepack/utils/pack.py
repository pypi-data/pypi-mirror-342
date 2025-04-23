import datetime
import fnmatch
import importlib.metadata
import json
import logging
import pathlib
import shutil

import ansiblecall
import ansiblecall._version

import ansiblepack
import ansiblepack._version
from ansiblepack.utils.process import Parallel

log = logging.getLogger(__name__)


class Packer(Parallel):
    def __init__(self, dest_dir, mod_name):
        self.mod_name = mod_name
        self.dest_dir = dest_dir

    @staticmethod
    def save_manifest(dest_dir):
        data = {}
        data["ansible"] = importlib.metadata.version("ansible")
        data["ansible-call"] = ansiblecall._version.__version__  # noqa: SLF001
        data["ansible-pack"] = ansiblepack._version.__version__  # noqa: SLF001
        data["timestamp"] = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        with open(pathlib.Path(dest_dir).joinpath("manifest.json"), "w") as fp:
            fp.write(json.dumps(data))

    @classmethod
    def pack(cls, dest_dir, modules=None, pattern=None):
        # Initialize dir
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Filter modules
        mods = list(ansiblecall.refresh_modules())
        pack_mods = set()
        if modules:
            pack_mods = set(modules) & set(mods)
        if pattern:
            for mod in mods:
                if fnmatch.fnmatch(mod, pattern):
                    pack_mods.add(mod)

        if not pack_mods:
            return

        # Parallelize packaging.
        tasks = [cls(dest_dir=dest_dir, mod_name=m) for m in pack_mods]
        cls.start(tasks=tasks)

        # Write a manifest.json file that contains the version, date created,
        # the input used for creation.
        cls.save_manifest(dest_dir=dest_dir)

        # Copy salt modules
        shutil.copytree(
            src=pathlib.Path(ansiblepack.__file__).parent.joinpath("salt"),
            dst=dest_dir,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )

    def run(self):
        """
        Package ansible modules as zip files
        """
        return ansiblecall.cache(mod_name=self.mod_name, dest=self.dest_dir)
