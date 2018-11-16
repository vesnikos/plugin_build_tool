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
    if config.get('help', 'dir', fallback=None) is None:
        return False
    if config.get('help', 'target', fallback=None) is None:
        return False


def install_files_list(config: ConfigParser) -> List[str]:
    python_files = config.get('files', 'python_files').split()
    main_dialog = config.get('files', 'main_dialog').split()
    extras = config.get('files', 'extras').split()
    # merge the file lists
    install_files = python_files + main_dialog + extras

    return install_files


def compile_files(config: ConfigParser):
    # Compile all ui and resource files

    # pyuic5 is needed to compile *.ui to .py
    if pyuic5_exec is None:
        print("pyuic5 is not in your path---unable to compile your ui files.")
        return None

    files_dict = {
        'compiled_ui_files': config.get('files', 'compiled_ui_files').split(),
        'res_files': config.get('files', 'resource_files').split()
    }

    ui_files = files_dict['compiled_ui_files']
    counter = 0
    for idx, ui in enumerate(ui_files, 1):
        ui_path = Path(ui)
        if ui_path.is_file():
            output = ui_path.with_suffix('.py')

            # compile if needed
            if file_changed(ui, output):
                input_ui_file = ui_path.as_posix()
                output_py_file = output.as_posix()
                click.secho(f"Compiling {input_ui_file} to {output_py_file}")
                subprocess.check_call([pyuic5_exec, '-o', output_py_file, input_ui_file])
                counter += 1
            else:
                click.secho("Skipping {0} (unchanged)".format(ui))
        else:
            click.secho("{0} does not exist---skipped".format(ui))

    click.secho("Compiled {0} UI files".format(counter))

    # check to see if we have pyrcc5
    if pyrcc5_exec is None:
        click.secho("pyrcc5 is not in your path---unable to compile your resource file(s)",
                    fg='red')
        return None

    res_files = files_dict['compiled_ui_files']
    counter = 0
    for res in res_files:
        rc_path = Path(res)
        if rc_path.is_file():
            output = rc_path.with_suffix('.py')

            if file_changed(res, output):
                input_rc_file = rc_path.as_posix()
                output_py_file = output.as_posix()
                print(f"Compiling {input_rc_file} to {output_py_file}")
                subprocess.check_call([pyrcc5_exec, '-o', input_rc_file, output_py_file])
                counter += 1
            else:
                print("Skipping {0} (unchanged)".format(res))
        else:
            print("{0} does not exist---skipped".format(res))
    print("Compiled {0} resource files".format(counter))
