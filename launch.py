# Copyright 2022 iiPython
# eDOS - Emulated Disk Operating System

# Load vendored modules
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "modules")))

# Modules
import os
from edos import Shell

# Initialization
root_directory = os.path.abspath(os.path.dirname(__file__))
Shell(root_directory).handle_input()
