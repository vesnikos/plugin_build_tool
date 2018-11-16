import os
import subprocess
from typing import List,Optional
from configparser import ConfigParser

import click

from .files import pyuic5_exec


def cfg_is_valid(config: ConfigParser) -> bool:
    """
    Check the pb_tool.cfg file for mandatory sections/files.
    Detect the plugin install path and presence of a suitable zip utilty.
    """

    if config.get('plugin', 'name', fallback=None) is None:
        return False
    if config.get('files', 'python_files', fallback=None) is None:
        return False
    if config.get('files', 'main_dialog', fallback=None) is None:
        return False
    if config.get('files', 'resource_files', fallback=None) is None:
        return False
    if config.get('files', 'extras', fallback=None) is None:
        return False
    if config.get('help', 'dir', fallback=None) is None:
        return False
    if config.get('help', 'target', fallback=None) is None:
        return False


def install_files_list(config: ConfigParser)-> List[str]:
    python_files = config.get('files', 'python_files').split()
    main_dialog = config.get('files', 'main_dialog').split()
    extras = config.get('files', 'extras').split()
    # merge the file lists
    install_files = python_files + main_dialog + extras

    return install_files


def compile_files(config: ConfigParser):
    # Compile all ui and resource files
    # TODO add changed detection
    # cfg = get_config(config)

    # check to see if we have pyuic5

    if pyuic5_exec is None:
        print("pyuic5 is not in your path---unable to compile your ui or rc files")
        return None

    files_dict = {
        'compiled_ui_files': config.get('files', 'compiled_ui_files').split()
        'res_files' : config.get('files', 'resource_files').split()
    }

    ui_files = files_dict['compiled_ui_files']
    counter = 0
    for idx, ui in enumerate(ui_files,1):
        if os.path.exists(ui):
            (base, ext) = os.path.splitext(ui)
            output = "{0}.py".format(base)
            if file_changed(ui, output):
                click.secho("Compiling {0} to {1}".format(ui, output))
                subprocess.check_call([pyuic5_exec, '-o', output, ui])
                counter += 1
            else:
                click.secho("Skipping {0} (unchanged)".format(ui))
        else:
            print("{0} does not exist---skipped".format(ui))
    print("Compiled {0} UI files".format(counter))

    # check to see if we have pyrcc5
    pyrcc5 = find_pyuic5()

    if pyrcc5 is None:
        click.secho(
                "pyrcc5 is not in your path---unable to compile your resource file(s)",
                fg='red')
    else:
        res_files = cfg.get('files', 'resource_files').split()
        res_count = 0
        for res in res_files:
            if os.path.exists(res):
                (base, ext) = os.path.splitext(res)
                output = "{0}.py".format(base)
                if file_changed(res, output):
                    print("Compiling {0} to {1}".format(res, output))
                    subprocess.check_call([pyrcc5, '-o', output, res])
                    res_count += 1
                else:
                    print("Skipping {0} (unchanged)".format(res))
            else:
                print("{0} does not exist---skipped".format(res))
        print("Compiled {0} resource files".format(res_count))