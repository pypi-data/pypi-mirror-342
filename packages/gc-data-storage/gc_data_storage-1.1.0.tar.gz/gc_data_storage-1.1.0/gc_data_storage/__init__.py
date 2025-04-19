#INIT FOR GC_DATA_STORAGE - updted 4/18/2025

from gc_data_storage.gc_data_storage import gc_data_storage

# Let users know if they're missing any of our hard dependencies
hard_dependencies = ("subprocess", "pkg_resources")
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(f"{dependency}: {e}")

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(missing_dependencies)
        +".\nPease install module(s) before proceeding."
    )

#install other packages if not installed
import pkg_resources
import subprocess
import os

def install_if_not_installed(modules):  
    uninstalled_packages = [p for p in modules if p not in sorted(["%s==%s" % (i.key, i.version) for i in pkg_resources.working_set])]
    uninstalled_packages_f = " ".join(uninstalled_packages)
    res = subprocess.run(['pip', 'install', '--upgrade', uninstalled_packages_f], capture_output=True)

print('Installing dependencies. You may need to restart your kernel afterwards.')
install_if_not_installed(modules = ['pyarrow', 'openpyxl', 'pandas', 'google-cloud', 'google-api-core', 'ipython'])
