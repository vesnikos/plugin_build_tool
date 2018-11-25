"""
/***************************************************************************
                                    qpbt
                 A tool for building and deploying QGIS plugins
                              -------------------
        begin                : 2014-09-24
        copyright            : (C) 2014 by GeoApt LLC
        email                : gsherman@geoapt.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
__version__ = "3.0.6"
__date__ = '2017-11-05'
__author__ = 'gsherman'

import os
import sys
import subprocess
import shutil
import errno
import glob
import urllib.request
import urllib.error
from configparser import ConfigParser
from string import Template
from distutils.dir_util import copy_tree
import webbrowser

from typing import Union
from pathlib import Path

import click

from utils import qgis_dst_plugin_folder
from utils.files import install_files, clean_deployment, compile_files


def __get_config(ini_file: Union[Path, str]) -> ConfigParser:
    ini_file = Path(ini_file)
    if not ini_file.is_file():
        click.secho('Configuration file was not found', color='red')
        sys.exit(1)

    configuration = ConfigParser()
    configuration.read_file(ini_file)

    return configuration


@click.group()
@click.pass_context
@click.option('--config', default='pb_tool.cfg',
              help='Name of the config file to use if other than pb_tool.cfg')
def cli(ctx):
    """Simple Python tool to compile and deploy a QGIS plugin.
    For help on a command use --help after the command:
    pb_tool deploy --help.

    pb_tool requires a configuration file (default: pb_tool.cfg) that
    declares the files and resources used in your plugin. Plugin Builder
    2.6.0 creates a config file when you generate a new plugin template.

    See http://g-sherman.github.io/plugin_build_tool for for an example config
    file. You can also use the create command to generate a best-guess config
    file for an existing project, then tweak as needed.
    
    Bugs and enhancement requests, see:
        https://github.com/g-sherman/plugin_build_tool
    """

    ctx.ensure_object(dict)
    configuration = __get_config(config)
    if cfg_is_valid(configuration) is False:
        return 1

    ctx.obj['configuration'] = configuration


# def get_install_files(cfg):
#     python_files = cfg.get('files', 'python_files').split()
#     main_dialog = cfg.get('files', 'main_dialog').split()
#     extras = cfg.get('files', 'extras').split()
#     # merge the file lists
#     install_files = python_files + main_dialog + compiled_ui(
#         cfg) + compiled_resource(cfg) + extras
#     #click.echo(install_files)
#     return install_files


@cli.command()
def version():
    """Return the version of pb_tool and exit"""
    click.echo("pb_tool {}, {}".format(__version__, __date__))
    return 0


@cli.command()
@click.option('--plugin_path', '-p', default=None,
              help='Specify the directory where to deploy your plugin if not using the standard location')
@click.option('--quick', '-q', is_flag=True,
              help='Do a quick install without compiling ui, resource, docs, \
              and translation files and exit')
@click.option('--no-confirm', '-y', is_flag=True,
              help='Don\'t ask for confirmation to overwrite existing files')
@click.pass_context
def deploy(ctx, plugin_path, quick, no_confirm):
    """Deploy the plugin to QGIS plugin directory using parameters in pb_tool.cfg"""

    configuration = ctx.obj['configuration']

    # The plugin is going to be deployed in either in the User specified folder, or the folder declared in the
    # ini file or the default QGIS addon folder

    qgis_dst_plugin_root = plugin_path \
                           or configuration.get('plugin', 'plugin_path', fallback=None) \
                           or qgis_dst_plugin_folder()

    plugin_name = configuration.get('plugin', 'name')

    qgis_dst_plugin_root = qgis_dst_plugin_root / plugin_name
    click.secho(f"Deploying to {qgis_dst_plugin_root}", fg='green')

    if quick:
        install_files(qgis_dst_plugin_root, configuration)
        click.secho(
            "Quick deployment complete---if you have problems with your"
            " plugin, try doing a full deploy.",
            fg='green')
        return 0

    clean_deployment(qgis_dst_plugin_root)
    click.secho(f"Deploying to {qgis_dst_plugin_root}", fg='green')
    # compile to make sure everything is fresh
    click.secho('Compiling to make sure install is clean', fg='green')
    compile_files(cfg)  # TODO
    build_docs()  # TODO
    install_files(qgis_dst_plugin_root, configuration)

    # deploy_files(config, plugin_path, quick=quick, confirm=not no_confirm)


# def deploy_files(config, plugin_path, confirm=True, quick=False):
#     """Deploy the plugin using parameters in pb_tool.cfg"""
#     # check for the config file
#     if not os.path.exists(config):
#         click.secho("Configuration file {0} is missing.".format(config),
#                     fg='red')
#     else:
#         cfg = get_config(config)
#         if not plugin_path:
#             plugin_path = get_plugin_directory(config)
#             if not plugin_path:
#                 click.secho("Unable to determine where to deploy your plugin", fg='red')
#                 return
#
#         plugin_dir = os.path.join(plugin_path, cfg.get('plugin', 'name'))
#
#         click.secho("Deploying to {}".format(plugin_dir), fg='green')
#         if quick:
#             click.secho("Doing quick deployment", fg='green')
#             install_files(plugin_dir, cfg)
#             click.secho(
#                 "Quick deployment complete---if you have problems with your"
#                 " plugin, try doing a full deploy.",
#                 fg='green')
#
#         else:
#             if confirm:
#                 print("""Deploying will:
#                 * Remove your currently deployed version
#                 * Compile the ui and resource files
#                 * Build the help docs
#                 * Copy everything to your {} directory
#                 """.format(plugin_dir))
#
#                 proceed = click.confirm("Proceed?")
#             else:
#                 proceed = True
#
#             if proceed:
#                 # clean the deployment
#                 clean_deployment(False, config)
#                 click.secho("Deploying to {0}".format(plugin_dir), fg='green')
#                 # compile to make sure everything is fresh
#                 click.secho('Compiling to make sure install is clean',
#                             fg='green')
#                 compile_files(cfg)
#                 build_docs()
#                 install_files(plugin_dir, cfg)


# def install_files2(plugin_dir, cfg):
#     errors = []
#     install_files = get_install_files(cfg)
#     # make the plugin directory if it doesn't exist
#     if not os.path.exists(plugin_dir):
#         os.mkdir(plugin_dir)
#
#     fail = False
#     for file in install_files:
#         click.secho("Copying {0}".format(file), fg='magenta', nl=False)
#         try:
#             shutil.copy(file, os.path.join(plugin_dir, file))
#             print("")
#         except Exception as oops:
#             errors.append(
#                 "Error copying files: {0}, {1}".format(file, oops.strerror))
#             click.echo(click.style(' ----> ERROR', fg='red'))
#             fail = True
#         extra_dirs = cfg.get('files', 'extra_dirs').split()
#         # print "EXTRA DIRS: {}".format(extra_dirs)
#     for xdir in extra_dirs:
#         click.secho("Copying contents of {0} to {1}".format(xdir, plugin_dir),
#                     fg='magenta',
#                     nl=False)
#         try:
#             copy_tree(xdir, "{0}/{1}".format(plugin_dir, xdir))
#             print("")
#         except Exception as oops:
#             errors.append(
#                 "Error copying directory: {0}, {1}".format(xdir, oops.message))
#             click.echo(click.style(' ----> ERROR', fg='red'))
#             fail = True
#     help_src = cfg.get('help', 'dir')
#     help_target = os.path.join(plugin_dir,
#                                cfg.get('help', 'target'))
#     click.secho("Copying {0} to {1}".format(help_src, help_target),
#                 fg='magenta',
#                 nl=False)
#     # shutil.copytree(help_src, help_target)
#     try:
#         copy_tree(help_src, help_target)
#         print("")
#     except Exception as oops:
#         errors.append("Error copying help files: {0}, {1}".format(
#             help_src, oops.message))
#         click.echo(click.style(' ----> ERROR', fg='red'))
#         fail = True
#     if fail:
#         print("\nERRORS:")
#         for error in errors:
#             print(error)
#         print("")
#         print(
#             "One or more files/directories specified in your config file\n"
#             "failed to deploy---make sure they exist or if not needed remove\n"
#             "them from the config. To ensure proper deployment, make sure your\n"
#             "UI and resource files are compiled. Using dclean to delete the\n"
#             "plugin before deploying may also help.")


def clean_deployment2(ask_first=True, config='pb_tool.cfg'):
    """ Remove the deployed plugin from the .qgis2/python/plugins directory
    """
    name = get_config(config).get('plugin', 'name')
    plugin_dir = os.path.join(get_plugin_directory(), name)
    if ask_first:
        proceed = click.confirm(
            'Delete the deployed plugin from {0}?'.format(plugin_dir))
    else:
        proceed = True

    if proceed:
        click.echo('Removing plugin from {0}'.format(plugin_dir))
        try:
            shutil.rmtree(plugin_dir)
            return True
        except OSError as oops:
            print('Plugin was not deleted: {0}'.format(oops.strerror))
    else:
        click.echo('Plugin was not deleted')
    return False


@cli.command()
def clean_docs():
    """
    Remove the built HTML help files from the build directory
    """
    if os.path.exists('help'):
        click.echo('Removing built HTML from the help documentation')
        if sys.platform == 'win32':
            makeprg = 'make.bat'
        else:
            makeprg = 'make'
        cwd = os.getcwd()
        os.chdir('help')
        subprocess.check_call([makeprg, 'clean'])
        os.chdir(cwd)
    else:
        print("No help directory exists in the current directory")


@cli.command()
@click.option('--config',
              default='pb_tool.cfg',
              help='Name of the config file to use if other than pb_tool.cfg')
def dclean(config):
    """ Remove the deployed plugin from the .qgis2/python/plugins directory
    """
    clean_deployment(True, config)


@cli.command()
@click.option('--config',
              default='pb_tool.cfg',
              help='Name of the config file to use if other than pb_tool.cfg')
def clean(config):
    """ Remove compiled resource and ui files
    """
    cfg = get_config(config)
    files = compiled_ui(cfg) + compiled_resource(cfg)
    click.echo('Cleaning resource and ui files')
    for file in files:
        try:
            os.unlink(file)
            print("Deleted: {0}".format(file))
        except OSError as oops:
            print("Couldn't delete {0}: {1}".format(file, oops.strerror))


@cli.command()
@click.option('--config',
              default='pb_tool.cfg',
              help='Name of the config file to use if other than pb_tool.cfg')
def compile(config):
    """
    Compile the resource and ui files
    """
    compile_files(get_config(config))


@cli.command()
def doc():
    """ Build HTML version of the help files using sphinx"""
    build_docs()


def build_docs():
    """ Build the docs using sphinx"""
    if os.path.exists('help'):
        click.echo('Building the help documentation')
        if sys.platform == 'win32':
            makeprg = 'make.bat'
        else:
            makeprg = 'make'
        cwd = os.getcwd()
        os.chdir('help')
        subprocess.check_call([makeprg, 'html'])
        os.chdir(cwd)
    else:
        print("No help directory exists in the current directory")


@cli.command()
@click.option('--config', default='pb_tool.cfg',
              help='Name of the config file to use if other than pb_tool.cfg')
def translate(config):
    """ Build translations using lrelease. Locales must be specified
    in the config file and the corresponding .ts file must exist in
    the i18n directory of your plugin."""
    possibles = ['lrelease', 'lrelease-qt4']
    for binary in possibles:
        cmd = check_path(binary)
        if cmd:
            break
    if not cmd:
        print("Unable to find the lrelease command. Make sure it is installed"
              "  and in your path.")
        if sys.platform == 'win32':
            print('You can get lrelease by installing'
                  ' the qt4-devel package in the Libs'
                  '\nsection of the OSGeo4W Advanced Install.')
    else:
        cfg = get_config(config)
        if check_cfg(cfg, 'files', 'locales'):
            locales = cfg.get('files', 'locales').split()
            if locales:
                for locale in locales:
                    (name, ext) = os.path.splitext(locale)
                    if ext != '.ts':
                        print('no ts extension')
                        locale = name + '.ts'
                    print(cmd, locale)
                    subprocess.check_call([cmd, os.path.join('i18n', locale)])
            else:
                print("No translations are specified in {0}".format(config))


@cli.command()
@click.option('--config',
              default='pb_tool.cfg',
              help='Name of the config file to use if other than pb_tool.cfg')
@click.option('--quick', '-q', is_flag=True,
              help='Do a quick packaging without dclean and deploy (plugin must have been previously deployed)')
@click.option('--compress-format', type=click.Choice(['zip', 'gz']), default='zip')
def zip(config, quick, compress_format):
    """ Package the plugin into a zip file
    suitable for uploading to the QGIS
    plugin repository"""

    # check to see if we can find zip or 7z
    zip = find_zip()

    zip_util = find_zip() or find_7z() or None
    if zip_util is None:
        click.secho('zip or 7z not found. Unable to package the plugin',
                    fg='red')
        click.secho('Check your path or install a zip program', fg='red')
    click.secho('Found zip: %s' % zip, fg='green')

    name = get_config(config).get('plugin', 'name', fallback=None)
    if not quick:
        proceed = click.confirm('This requires a dclean and deploy first. Proceed?')
        if proceed:
            # clean_deployment(False, config)
            deploy_files(config, plugin_path=None, confirm=False)
    else:
        # Check to see if the plugin directory exists, otherwise we can't
        # do a quick zip
        if not os.path.exists(os.path.join(get_plugin_directory(), name)):
            # click.secho(
            #     "You must deploy the plugin before you can package it using -q",
            #     fg='red')
            # proceed = click.confirm(
            #     'Do you want to deploy and proceed with packaging?')
            # if proceed:
            deploy_files(config, plugin_path=None, confirm=False)
        proceed = True

    # confirm = click.confirm(
    #    'Create a packaged plugin ({0}.zip) from the deployed files?'.format(name))
    # confirm = True
    if proceed:
        # delete the zip if it exists
        if os.path.exists('{0}.zip'.format(name)):
            os.unlink('{0}.zip'.format(name))
        if name:
            cwd = os.getcwd()
            os.chdir(get_plugin_directory())
            # click.secho("Current directory is {}".format(os.getcwd()), fg='magenta')
            if use_7z:
                subprocess.check_call(
                    [zip, 'a', '-r', os.path.join(cwd, '{0}.zip'.format(name)),
                     name])
            else:
                subprocess.check_call([
                    zip, '-r', os.path.join(cwd, '{0}.zip'.format(name)), name
                ])

            print(
                'The {0}.zip archive has been created in the current directory'.format(
                    name))
        else:
            click.echo(
                "Your config file is missing the plugin name (name=parameter)")


@cli.command()
@click.option('--config',
              default='pb_tool.cfg',
              help='Name of the config file to use if other than pb_tool.cfg')
@cli.command()
@click.option('--config',
              default='pb_tool.cfg',
              help='Name of the config file to use if other than pb_tool.cfg')
def list(config):
    """ List the contents of the configuration file """
    if os.path.exists(config):
        with open(config) as cfg:
            for line in cfg:
                print(line[:-1])
    else:
        click.secho(
            "There is no {0} file in the current directory".format(config),
            fg='red')
        click.secho("We can't do anything without it", fg='red')


@cli.command()
# @click.option(
#     '--modulename',
#     prompt=True,
#     help='Name of the module for the new plugin. Lower case with underscores, e.g: my_plugin')
# @click.option(
#     '--classname',
#     prompt=True,
#     help='Class name for the new plugin. CamelCase, no underscores, e.g: MyPlugin')
# @click.option(
#     '--menutext',
#     prompt=True,
#     help='Text for the menu.')
def create(modulename=None, classname=None, menutext=None):
    """ Create a new plugin in the current directory using either the basic or dialog template. """
    # print("Creating {} in module {} with menu text {}".format(classname, modulename, menutext))
    print("This feature is not implemented yet")


@cli.command()
@click.option(
    '--name',
    default='pb_tool.cfg',
    help='Name of the config file to create if other than pb_tool.cfg')
@click.option(
    '--package',
    default=None,
    help='Name of package (lower case). This will be used as the directory name for deployment')
def config(name, package):
    """
    Create a config file based on source files in the current directory
    """
    click.secho("Create a config file based on source files in the current directory", fg="green")
    if name == 'pb_tool.cfg':
        click.secho("This will overwrite any existing pb_tool.cfg in the current directory", fg="red")
        proceed = click.confirm('Proceed?')
        if not proceed:
            return
    template = Template(config_template())
    # get the plugin package name

    if not package:
        cfg_name = click.prompt('Name of package (lower case). This will be used as the directory name for deployment')
    else:
        cfg_name = name

    # get the list of python files
    py_files = glob.glob('*.py')

    # guess the main dialog ui file
    main_dlg = glob.glob('*_dialog_base.ui')

    # get the other ui files
    other_ui = glob.glob('*.ui')
    # remove the main dialog file
    try:
        for ui in main_dlg:
            other_ui.remove(ui)
    except:
        # don't care if we didn't find it
        pass

    # get the resource files (.qrc)
    resources = glob.glob("*.qrc")

    extras = glob.glob('*.png') + glob.glob('metadata.txt')

    locale_list = glob.glob('i18n/*.ts')
    locales = []
    for locale in locale_list:
        locales.append(os.path.basename(locale))

    cfg = template.substitute(Name=cfg_name,
                              PythonFiles=' '.join(py_files),
                              MainDialog=' '.join(main_dlg),
                              CompiledUiFiles=' '.join(other_ui),
                              Resources=' '.join(resources),
                              Extras=' '.join(extras),
                              Locales=' '.join(locales))

    fname = name
    if os.path.exists(fname):
        confirm = click.confirm('{0} exists. Overwrite?'.format(name))
        if not confirm:
            fname = click.prompt('Enter a name for the config file:')

    with open(fname, 'w') as f:
        f.write(cfg)

    print("Created new config file in {0}".format(fname))


@cli.command()
def update():
    """ Check for update to pb_tool """
    try:
        u = urllib.request.urlopen('http://geoapt.net/pb_tool/current3_version.txt')
        version = str(u.read()[:-1], 'utf-8')
        click.secho("Latest version is %s" % version, fg='green')
        this_version = int(__version()[0].replace('.', ''))
        current_version = int(version.replace('.', ''))

        if this_version == current_version:
            click.secho("Your version is up to date", fg='green')
        elif current_version > this_version:
            click.secho("You have Version %s" % __version()[0], fg='green')
            click.secho("You can upgrade by running this command:")
            cmd = 'pip install --upgrade pb_tool'
            print("   %s" % cmd)
        elif this_version > current_version:
            click.secho("You have development version {}".format(__version()[0]), fg='green')

    except urllib.error.URLError as uoops:
        click.secho("Unable to check for update.")
        click.secho("%s" % uoops.reason)


@cli.command()
def help():
    "Open the pb_tools web page in your default browser"
    webbrowser.open_new('http://g-sherman.github.io/plugin_build_tool')
    return 0


def check_cfg(cfg, section, name):
    try:
        cfg.get(section, name)
        return True
    except configparser.NoOptionError as oops:
        print(oops.message)
    except configparser.NoSectionError:
        print("Missing section '{0}' when looking for option '{1}'".format(
            section, name))
    return False


def get_config(config='pb_tool.cfg'):
    """
    Read the config file pb_tools.cfg and return it
    """
    if os.path.exists(config):
        cfg = configparser.ConfigParser()
        cfg.read(config)
        # click.echo(cfg.sections())
        return cfg
    else:
        print("There is no {0} file in the current directory".format(config))
        print("We can't do anything without it")
        sys.exit(1)


def compiled_ui(cfg):
    # cfg = get_config(config)
    try:
        uis = cfg.get('files', 'compiled_ui_files').split()
        compiled = []
        for ui in uis:
            (base, ext) = os.path.splitext(ui)
            compiled.append('{0}.py'.format(base))
        # print "Compiled UI files: {}".format(compiled)
        return compiled
    except configparser.NoSectionError as oops:
        print(oops.message)
        sys.exit(1)


def compiled_resource(cfg):
    # cfg = get_config(config)
    try:
        res_files = cfg.get('files', 'resource_files').split()
        compiled = []
        for res in res_files:
            (base, ext) = os.path.splitext(res)
            compiled.append('{0}.py'.format(base))
        # print "Compiled resource files: {}".format(compiled)
        return compiled
    except configparser.NoSectionError as oops:
        print(oops.message)
        sys.exit(1)


# def compile_files2(cfg):
#     # Compile all ui and resource files
#     # TODO add changed detection
#     # cfg = get_config(config)
#
#     # check to see if we have pyuic5
#     pyuic5 = find_pyuic5()
#
#     if pyuic5 is None:
#         print("pyuic5 is not in your path---unable to compile your ui files")
#     else:
#         ui_files = cfg.get('files', 'compiled_ui_files').split()
#         ui_count = 0
#         for ui in ui_files:
#             if os.path.exists(ui):
#                 (base, ext) = os.path.splitext(ui)
#                 output = "{0}.py".format(base)
#                 if file_changed(ui, output):
#                     print("Compiling {0} to {1}".format(ui, output))
#                     subprocess.check_call([pyuic5, '-o', output, ui])
#                     ui_count += 1
#                 else:
#                     print("Skipping {0} (unchanged)".format(ui))
#             else:
#                 print("{0} does not exist---skipped".format(ui))
#         print("Compiled {0} UI files".format(ui_count))
#
#     # check to see if we have pyrcc5
#     pyrcc5 = find_pyuic5()
#
#     if pyrcc5 is None:
#         click.secho(
#             "pyrcc5 is not in your path---unable to compile your resource file(s)",
#             fg='red')
#     else:
#         res_files = cfg.get('files', 'resource_files').split()
#         res_count = 0
#         for res in res_files:
#             if os.path.exists(res):
#                 (base, ext) = os.path.splitext(res)
#                 output = "{0}.py".format(base)
#                 if file_changed(res, output):
#                     print("Compiling {0} to {1}".format(res, output))
#                     subprocess.check_call([pyrcc5, '-o', output, res])
#                     res_count += 1
#                 else:
#                     print("Skipping {0} (unchanged)".format(res))
#             else:
#                 print("{0} does not exist---skipped".format(res))
#         print("Compiled {0} resource files".format(res_count))


def copy(source, destination):
    """Copy files recursively.

    Taken from: http://www.pythoncentral.io/
                how-to-recursively-copy-a-directory-folder-in-python/

    :param source: Source directory.
    :type source: str

    :param destination: Destination directory.
    :type destination: str

    """
    try:
        # shutil.copytree(source, destination)
        copy_tree(source, destination)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(source, destination)
        else:
            print('Directory not copied. Error: %s' % e)


def get_plugin_directory_old(config='pb_tool.cfg'):
    """ Get the plugin directory, first checking to see if it's configured in pb_tool.cfg"""
    plugin_dir = get_config(config).get('plugin', 'plugin_path', fallback=None)

    if plugin_dir:
        click.secho("Using plugin directory from pb_tool.cfg", fg='green')
    else:
        try:
            from PyQt5.QtCore import QStandardPaths, QDir
            path = QStandardPaths.standardLocations(QStandardPaths.AppDataLocation)[0]
            plugin_dir = os.path.join(QDir.homePath(), path, 'QGIS/QGIS3/profiles/default/python/plugins')
            # click.secho("Plugin path: {}".format(plugin_path), fg='green')
        except:
            click.secho("""Unable to determine location of your QGIS Plugin directory.
            Make sure your QGIS environment is setup properly for development and Python
            has access to the PyQt5.QtCore module or specify plugin_path in your pb_tool.cfg.""", fg='red')
            plugin_dir = None

    return plugin_dir


def config_template():
    """
    :return: the template for a pb_tool.cfg file
    """
    template = """# Configuration file for plugin builder tool
# Sane defaults for your plugin generated by the Plugin Builder are
# already set below.
#
# As you add Python source files and UI files to your plugin, add
# them to the appropriate [files] section below.

[plugin]
# Name of the plugin. This is the name of the directory that will
# be created when deployed
name: $Name

# Full path to where you want your plugin directory copied. If empty,
# the QGIS default path will be used. Don't include the plugin name in
# the path.
plugin_path:

[files]
# Python  files that should be deployed with the plugin
python_files: $PythonFiles

# The main dialog file that is loaded (not compiled)
main_dialog: $MainDialog

# Other ui files for your dialogs (these will be compiled)
compiled_ui_files: $CompiledUiFiles

# Resource file(s) that will be compiled
resource_files: $Resources

# Other files required for the plugin
extras: $Extras

# Other directories to be deployed with the plugin.
# These must be subdirectories under the plugin directory
extra_dirs:

# ISO code(s) for any locales (translations), separated by spaces.
# Corresponding .ts files must exist in the i18n directory
locales: $Locales

[help]
# the built help directory that should be deployed with the plugin
dir: help/build/html
# the name of the directory to target in the deployed plugin
target: help
"""

    return template


def check_path(app):
    """ Adapted from StackExchange:
        http://stackoverflow.com/questions/377017
    """
    import os

    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    def ext_candidates(fpath):
        yield fpath
        for ext in os.environ.get("PATHEXT", "").split(os.pathsep):
            yield fpath + ext

    fpath, fname = os.path.split(app)
    if fpath:
        if is_exe(app):
            return app
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, app)
            for candidate in ext_candidates(exe_file):
                if is_exe(candidate):
                    return candidate

    return None


def file_changed(infile, outfile):
    try:
        infile_s = os.stat(infile)
        outfile_s = os.stat(outfile)
        return infile_s.st_mtime > outfile_s.st_mtime
    except:
        return True
