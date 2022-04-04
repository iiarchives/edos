# Copyright 2022 iiPython

# Modules
import os
import atexit
import shutil
import tarfile
import tempfile
from typing import Any, List

# Initialization
open_ = open
disk_location = os.environ.get("EDOS_DISK")

# Helper functions
def resolve(p: str) -> str:
    if p[0] == "/":
        return os.path.join(disk_location, p[1:])

    return os.path.abspath(os.path.join(os.getcwd(), p))

def open(p: str, *args, **kwargs) -> Any:
    return open_(resolve(p), *args, **kwargs)

def listdir(p: str = None) -> List[Any]:
    return os.listdir(resolve(p) if p else os.getcwd())

for f in ["isfile", "isdir", "islink", "exists"]:
    globals()[f] = lambda p: getattr(os.path, f)(resolve(p))

# Filesystem class
class Filesystem(object):
    def __init__(self, disk_file: str) -> None:
        self.disk_file = disk_file
        self.disk_location = os.path.join(tempfile.gettempdir(), "edos_disk")

        os.environ["EDOS_DISK"] = self.disk_location

        # Handle first-time initialization
        initial_disk_location = os.path.join(os.path.dirname(self.disk_file), "disk")
        if os.path.isdir(initial_disk_location):
            self.recompress_disk(initial_disk_location)

        self.decompress_disk()
        atexit.register(self.recompress_disk)

    def decompress_disk(self) -> None:
        if not os.path.isdir(self.disk_location):
            os.mkdir(self.disk_location)

        if os.path.isfile(self.disk_file):
            with tarfile.open(self.disk_file, "r:gz") as disk:
                disk.extractall(self.disk_location)

    def recompress_disk(self, directory: str = None) -> None:
        if directory is None:
            directory = self.disk_location

        with tarfile.open(self.disk_file, "w:gz") as disk:
            disk.add(directory, "")

        shutil.rmtree(directory)
