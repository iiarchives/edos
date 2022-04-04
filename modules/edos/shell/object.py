# Copyright 2022 iiPython

# Modules
import os
from edos.fs import Filesystem

# Shell class
class Shell(object):
    def __init__(self, root: str) -> None:
        self.fs = Filesystem(os.path.join(root, "disk.edos"))
        os.chdir(self.fs.disk_location)

    def handle_input(self) -> None:
        return
