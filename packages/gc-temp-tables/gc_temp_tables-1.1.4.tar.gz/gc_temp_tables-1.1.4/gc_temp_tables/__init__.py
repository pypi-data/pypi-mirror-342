#INIT FOR GC_TEMP_TABLES - updated 4/18/2025

from gc_temp_tables import gc_temp_tables

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

#Install other packages if not installed.
def install_if_not_installed(modules):  
    uninstalled_packages = [p for p in modules if p not in sorted(["%s==%s" % (i.key, i.version) for i in pkg_resources.working_set])]
    uninstalled_packages_f = " ".join(uninstalled_packages)
    res = subprocess.run(['pip', 'install', '--upgrade', uninstalled_packages_f], capture_output=True)

install_if_not_installed(modules = ['google-cloud'])

import os
from google.cloud import bigquery
client = bigquery.Client()
