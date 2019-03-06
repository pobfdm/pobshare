##usage python freeze.py build

import sys, os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os","sys", "utils", "guiUtils"], "excludes": ["tkinter"]}


exe1 = Executable(
    script = "pobshare.py",
    targetName = "pobshare.exe",
    icon = "icons"+os.sep+"pobshare.ico",
    base = "Win32GUI",
)



setup(  name = "pobshare",
        version = "0.1",
        description = "Share your folders!",
        options = {"build_exe": build_exe_options},
        executables = [exe1]
        )
