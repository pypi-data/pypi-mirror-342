"""
standard package import
"""
import os
from importlib import resources
from typing import Any, List, Dict, Union
from os import path

def main() -> str:
    """Return path to config file"""
    conf_file_name = "busstop_config.ini"
    if "BUSSTOP_HOME" in os.environ:
        return os.environ[f"BUSSTOP_HOME/{conf_file_name}"]
    home_dir = path.expanduser("~")
    if path.isfile(f"{home_dir}/{conf_file_name}"):
        return f"{home_dir}/{conf_file_name}"
    package_path = resources.files(__package__)
    return path.join(str(package_path), f"config/{conf_file_name}")


if __name__ == "__main__":
    main()
