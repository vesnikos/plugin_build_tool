import shutil
import subprocess
from distutils.dir_util import copy_tree
from pathlib import Path
from typing import Union, List

from configparser import ConfigParser

import click
from whichcraft import which


def find_zip():
    zip = which('zip')
    return zip


def find_pyrcc5():
    pyrcc5 = which('pyrcc5')
    return pyrcc5


def find_pyuic5():
    pyuic5 = which('pyuic5')
    return pyuic5


def find_7z():
    # check for 7z
    _7z = which('7z')
    return _7z


pyuic5_exec = find_pyuic5()
pyrcc5_exec = find_pyrcc5()
zip_exec = find_zip()


def file_changed(this: Union[str, Path], other: Union[str, Path]) -> bool:
    this_st_mtime = Path(this).stat().st_mtime
    other_st_mtime = Path(other).stat().st_mtime
    return this_st_mtime > other_st_mtime


def install_files(qgis_dst_plugin_root: Union[Path, str], config: ConfigParser):
    """
    Copies the files to QGIS for usage.

    :param qgis_dst_plugin_root: The destination in QGIS plugin folder where plugin is going to be copied.
    :param config: Pb_tool configuration Object
    :type config: ConfigParser
    """
    qgis_dst_plugin_root = Path(qgis_dst_plugin_root)

    errors = []
    failed = False
    install_files_manifest = install_files_dict(config)

    # make the plugin directory if it doesn't exist
    if not qgis_dst_plugin_root.is_dir():
        qgis_dst_plugin_root.mkdir()

    for category in install_files_manifest.keys():
        click.secho(f'Copying {category}.')

        for file in install_files_manifest.get(category):
            click.secho(f"Copying {file}", fg='magenta', nl=False)
            try:
                # src, dst
                shutil.copy(file, qgis_dst_plugin_root / file)
                print("")
            except Exception as oops:
                errors.append(
                    f"Error copying files: {file}, {oops.strerror}")
                click.echo(click.style(' ----> ERROR', fg='red'))
                failed = True

    # Other directories to be deployed with the plugin.
    # These must be subdirectories under the plugin directory
    extra_dirs = config.get('files', 'extra_dirs', ).split()
    for xdir in extra_dirs:
        click.secho("Copying contents of {0} to {1}".format(xdir, qgis_dst_plugin_root),
                    fg='magenta',
                    nl=False)
        try:
            # src, dst
            copy_tree(xdir, "{0}/{1}".format(qgis_dst_plugin_root, xdir))
            print("")
        except Exception as oops:
            errors.append(
                "Error copying directory: {0}, {1}".format(xdir, oops.message))
            click.echo(click.style(' ----> ERROR', fg='red'))
            failed = True

    # help::dir -> the built help directory in the src_folder that should be deployed with the plugin
    # Not mandatory, skip if not set.
    help_src_dir = config.get('help', 'dir', fallback=None)
    if help_src_dir is not None:

        # help::target -> # the name of the directory to target in the deployed plugin
        # optional: if set use that path, if not default to 'Help'
        help_dst_dir = config.get('help', 'target', fallback=None) or 'Help'
        help_dst_dir = qgis_dst_plugin_root / help_dst_dir

        click.secho(f"Copying {help_src_dir} to {help_dst_dir}", fg='magenta', nl=False)

        try:
            copy_tree(help_src_dir, help_dst_dir)
            print("")
        except Exception as oops:
            errors.append(f"Error copying help files: {help_src_dir}, {oops.message}")
            click.echo(click.style(' ----> ERROR', fg='red'))
            failed = True

    if failed:
        print("\nERRORS:")
        for error in errors:
            print(error)
        print("")
        print(
            "One or more files/directories specified in your config file\n"
            "failed to deploy---make sure they exist or if not needed remove\n"
            "them from the config. To ensure proper deployment, make sure your\n"
            "UI and resource files are compiled. Using dclean to delete the\n"
            "plugin before deploying may also help.")


def clean_deployment(qgis_dst_plugin_root: Union[Path, str]) -> bool:
    """ Remove the folder in the plugin directory
    """
    proceed = click.confirm(f'Delete the deployed plugin from {qgis_dst_plugin_root}?')

    if proceed:
        click.echo(f'Removing plugin from {qgis_dst_plugin_root}')
        try:
            shutil.rmtree(qgis_dst_plugin_root)
            return True
        except OSError as oops:
            print('Plugin was not deleted: {0}'.format(oops.strerror))
    else:
        click.echo('Plugin was not deleted')
    return False


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


def compile_ui(input_ui_file: Path, output_py_file: Path=None):
    """ Compiles the ui to py. If output name is not defined it is taken from the input name """

    output_py_file = output_py_file or input_ui_file.with_suffix('.py')

    output_py_file = output_py_file.as_posix()
    input_ui_file = input_ui_file.as_posix()

    subprocess.check_call([pyuic5_exec, '-o', output_py_file, input_ui_file])
