# Copyright 2022 iiPython

# Modules
import os
import json
from edos import fs

# Path handling class
class PathHandler(object):
    def __init__(self) -> None:
        self.path = []
        self.path_file = fs.resolve("/System/Settings/system_path")

        self.load()

    def load(self) -> None:
        if os.path.isfile(self.path_file):
            self.path = [itm for itm in open(self.path_file, "r").read().splitlines() if not itm.startswith("#") and itm.strip()]

    def resolve(self, path: str) -> str | None:
        for sp in self.path + [fs.getcwd()]:
            fp = fs.resolve(sp)
            for item in os.listdir(fp):
                itempath = os.path.join(fp, item)
                if item == path:
                    if os.path.isfile(itempath):
                        return itempath

                    elif os.path.isdir(itempath):
                        meta_path = os.path.join(itempath, "binary_meta.json")
                        if os.path.isfile(meta_path):
                            try:
                                metadata = json.loads(open(meta_path, "r").read())
                                if os.name in metadata:
                                    return os.path.abspath(os.path.join(itempath, metadata[os.name]))

                            except Exception:
                                pass
