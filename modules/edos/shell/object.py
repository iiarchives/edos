# Copyright 2022 iiPython

# Modules
import os
import shlex
from iipython.iikp import readchar, keys

from edos import fs

# Shell class
class Shell(object):
    def __init__(self, root: str) -> None:
        self.fs = fs.Filesystem(os.path.join(root, "disk.edos"))
        os.chdir(self.fs.disk_location)

    def autocomplete(self, value: str) -> str:
        value = value.strip("\"")
        if value.startswith("/"):
            path = fs.resolve("/".join(value.split("/")[:-1]) or "/")
            if os.path.isdir(path):
                for file in os.listdir(path):
                    if file.lower().startswith(value.lower().split("/")[-1]):
                        fp = fs.clean(os.path.abspath(os.path.join(path, file)))
                        return fp if " " not in fp else f"\"{fp}\""

    def readline(self, prompt: str) -> str:
        command, last_size = "", 0
        while True:
            prefix = f"{' ' * (last_size + 2)}\r" if len(command) < last_size else ""
            print(f"\r{prefix}{prompt}{command}", end = "")
            last_size = len(command)

            # Handle keypress
            kp = readchar()
            if kp == "\t":
                try:
                    chunks = shlex.split(command, posix = False)

                except ValueError:
                    try:
                        chunks = shlex.split(command + "\"", posix = False)

                    except Exception:
                        chunks = None

                if chunks is not None:
                    chunks[-1] = self.autocomplete(chunks[-1])
                    if chunks[-1] is not None:
                        command = " ".join(chunks)

            elif isinstance(kp, str):
                command += kp

            elif kp == keys.ENTER:
                print()
                return command

            elif kp == keys.CTRL_C:
                raise KeyboardInterrupt

            elif kp == keys.BACKSPACE and command:
                command = command[:-1]

    def handle_input(self) -> None:
        while True:
            print(self.readline(f"{fs.getcwd()} $ "))
