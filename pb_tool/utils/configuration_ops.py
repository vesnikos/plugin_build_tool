import subprocess
from pathlib import Path
from typing import List
from configparser import ConfigParser

import click

from .files import pyuic5_exec, pyrcc5_exec, file_changed


def cfg_is_valid(config: ConfigParser) -> bool:
    """
    Check the pb_tool.cfg file for mandatory sections.
    """

    plugin_name = config.get('plugin', 'name', fallback=None)
    if plugin_name is None:
        return False

    # Check if the files::python_files is set, and if they point to a valid file
    python_files = config.get('files', 'python_files', fallback=None)
    if python_files is None:
        return False
    for py_file in python_files:
        temp_path = Path(py_file)
        if not temp_path.is_file():
            msg = f"File {temp_path} was not found."
            click.secho(msg,color='red')
            return False

    if config.get('files', 'main_dialog', fallback=None) is None:
        return False
    if config.get('files', 'resource_files', fallback=None) is None:
        return False
    if config.get('files', 'extras', fallback=None) is None:
        return False
    # Help dir should not be mandatory
    # if config.get('help', 'dir', fallback=None) is None:
    #     return False
    # if config.get('help', 'target', fallback=None) is None:
    #     return False
