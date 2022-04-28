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
            ".": self.pathref,
            "exit": lambda *a: os._exit(0)
        }

    def cd(self, shell, args: list) -> None:
        if not args:
            return os.chdir(fs.resolve("/"))

        try:
            os.chdir(fs.resolve(args[0]))

        except FileNotFoundError:
            return print("cd: no such directory")

    def set(self, shell, args: list) -> None:
        if len(args) != 2:
            return print("usage: set <var> <value>")

        shell.env[args[0]] = args[1]

    def pathref(self, shell, args: list) -> None:
        if args:
            if not fs.isfile(args[0]):
                return print("source: no such path file exists")

            shell.path.path_file = fs.resolve(args[0])

        shell.path.load()
