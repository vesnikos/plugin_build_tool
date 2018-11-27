import platform
import subprocess

from pathlib import Path

from pb_tool.utils.files import pyrcc5_exec, pyuic5_exec


def qgis_plugin_folder(profile='default') -> Path:
    """ The QGIS master Plugin folder """

    # caveat: env variable QGIS_PLUGINPATH overrides everything?

    # Standard locations are listed at
    # https://docs.qgis.org/testing/en/docs/user_manual/plugins/plugins.html
    user_home_path = Path('~')

    os = platform.system()
    if os == 'Windows':
        qgis_user_profile = Path(r'AppData\Roaming\QGIS\QGIS3\profiles')
    elif os == 'Linux':
        qgis_user_profile = Path('.local/share/QGIS/QGIS3/profiles')
    elif os == 'Darwin':  # MacOS?
        qgis_user_profile = Path('Library/Application Support/QGIS/QGIS3/profiles')
    else:
        raise NotImplemented('Could not detectect the OS system.')

    plugin_folder = Path(f'{profile}/python/plugins')
    res = Path(user_home_path / qgis_user_profile / plugin_folder).expanduser()

    return res


# TODO: make test
def compile_qt_file(input_file: Path, output_file: Path, ftype: str):
    if ftype == 'ui':
        exec = pyuic5_exec
    elif ftype == 'qrc':
        exec = pyrcc5_exec
    else:
        raise ValueError('ftype must be either ui or qrc.')

    if exec is None:
        raise ValueError('compiling software could no be found.')

    if not input_file.is_file():
        raise ValueError(f'{input_file.name} is not a file')
    input_file = input_file.as_posix()
    output_file = output_file.as_posix()
    subprocess.check_call([pyuic5_exec, '-o', output_file, input_file])


qgis_default_plugin_folder = qgis_plugin_folder()
