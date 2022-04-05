# Copyright 2022 iiPython
# eDOS Standard Library Macros

# Modules
import os
from edos import fs

# Standard library class
class StandardLib(object):
    def __init__(self) -> None:
        self.macros = {
            "cd": self.cd,
            "set": self.set,
            "exit": lambda *a: os._exit(0)
        }

    def cd(self, shell, args: list) -> None:
        if not args:
            return os.chdir(fs.resolve("/"))

        os.chdir(fs.resolve(args[0]))

    def set(self, shell, args: list) -> None:
        if len(args) != 2:
            return print("usage: set <var> <value>")

        shell.env[args[0]] = args[1]
