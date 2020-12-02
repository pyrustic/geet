import os.path
from geet import about


#
USER_AGENT = ("User-Agent", "Pyrustic")

#
PYRUSTIC_DATA = os.path.join(os.path.expanduser("~"), "PyrusticData")

#
GEET_SHARED_FOLDER = os.path.join(PYRUSTIC_DATA, "geet")
GEET_SHARED_DATA_FILE = os.path.join(GEET_SHARED_FOLDER,
                                    "geet_shared_data.json")
DEFAULT_GEET_SHARED_DATA_FILE = os.path.join(about.ROOT_DIR,
                                            "default_shared_data.json")
DEFAULT_GEET_APPS_LIST_FILE = os.path.join(about.ROOT_DIR,
                                          "default_apps_list_data.json")
#
ABOUT_JSON_FILE = os.path.join(about.ROOT_DIR, "pyrustic_data", "about.json")

#
