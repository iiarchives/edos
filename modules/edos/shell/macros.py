# Copyright 2022 iiPython

# Modules
import os
import inspect
import importlib.util

from edos import fs

# Macro loading class
class MacroLoader(object):
    def __init__(self) -> None:
        self.module_directory = fs.resolve("/System/Modules")

    def get_macros(self, file: str) -> dict:
        spec = importlib.util.spec_from_file_location(file.split("/")[-1].removesuffix(".py"), file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Try to find macros
        macros = {}
        for n, class_ in inspect.getmembers(module, inspect.isclass):
            try:
                cl = class_()
                if hasattr(cl, "macros"):
                    macros = macros | cl.macros

            except Exception as e:
                print(e)

        return macros

    def as_dict(self) -> dict:
        macros = {}
        for path, _, files in os.walk(self.module_directory):
            for file in [f for f in files if f.endswith(".py") and f[0] != "_"]:
                fp = os.path.join(path, file)
                try:
                    macros = macros | self.get_macros(fp)

                except Exception:
                    print(f"eDOS: failed while loading macros in file '{file}'")

        return macros
