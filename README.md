# <img style = "float: right;" height = "40" src = "/images/eDOS.png"> eDOS

### the Emulated Disk Operating System
***

## Introduction

eDOS is a Python-based "Operating System" similiar in design to [DOS](https://en.wikipedia.org/wiki/DOS). Its principle design revolves around all system files being compressed to a disk image and uncompressed as needed at runtime. This allows for eDOS installs to be completely portable and debuggable.  

Is it a real operating system?  
**No. eDOS is just an isolated system with a command shell.**  

So, what's the point of it then?  
eDOS is meant to be ran on embedded systems, as it can run smoothly with little overhead. It could be referred to as an more-isolated clone of [Bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)), but eDOS is more about making a fully functioning system rather than just a shell.

## Pre-install notices

In case it wasn't already clear, eDOS uses a [gzipped](https://en.wikipedia.org/wiki/Gzip) [tarball](https://en.wikipedia.org/wiki/Tar_(computing)) to store its filesystem. It is important to make sure you have the CPU requirements to handle compressing/decompressing the archive at runtime and that you have enough physical disk space to do so as well.  

The following are needed before continuing with the install:
+ **Python 3.10 or above** (you can get the latest release from the [Python website](https://python.org))
+ Git SCM (optional, download [here](https://git-scm.com))

## Installation

The following steps should allow you to setup a basic eDOS system.  
Please note that **these steps are platform-dependent**, you might have to run different commands on your system.
+ Clone the eDOS repository with `git clone https://github.com/iiPythonx/edos`
    + If you don't have Git installed, you can also [download the ZIP](https://github.com/iiPythonx/edos/archive/refs/heads/master.zip)
    + The rest of these steps assume you have also entered the cloned `edos` folder
+ Ensure that [Python Magic](https://github.com/ahupp/python-magic) is setup correctly on your system
    + You can do this by running `python3 -c 'import modules.magic'`
    + Windows users will need to remove the `modules/magic` folder and replace it with an install of [python-magic-bin](https://github.com/julian-r/python-magic).

## Launching eDOS

After eDOS is setup, running it is as simple as launching `launch.py`.  
If you're having issues with disk building, you can specify the `--use-disk-folder` parameter, which will load the filesystem directly rather than building `disk.edos`.
