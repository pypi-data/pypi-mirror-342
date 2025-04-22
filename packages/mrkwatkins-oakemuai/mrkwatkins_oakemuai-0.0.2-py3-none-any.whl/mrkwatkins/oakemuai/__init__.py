from os import path

# Force __init__ to run from mrkwatkins.oakemu to initialise the CLR.
import mrkwatkins.oakemu  # noqa: F401

# Explicitly load all the necessary assemblies up front to help catch any errors early.
assembles = [
    "VYaml",
    "VYaml.Annotations",
    "MrKWatkins.OakEmu.Machines.ZXSpectrum.AI",
]

assemblies_path = path.join(path.dirname(__file__), "assemblies")

import clr  # noqa: E402

for assembly in assembles:
    clr.AddReference(path.join(assemblies_path, assembly))  # noqa
