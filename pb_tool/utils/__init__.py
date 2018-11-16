import platform

from pathlib import Path

from .configuration_ops import cfg_is_valid, install_files_list
from .find_qgis_dir import qgis_plugin_dir

__all__ = ['cfg_is_valid', 'qgis_plugin_dir', 'install_files_list', 'get_qgis_plugin_directory']


def get_qgis_plugin_directory(profile='default') -> Path:

    # caveat: env variable QGIS_PLUGINPATH overrides everything?

    # Standard locations are listed at
    # https://docs.qgis.org/testing/en/docs/user_manual/plugins/plugins.html
    user_home_path = Path('~')

    os = platform.system()
    if os == 'Windows':
        qgis_user_profile = Path('AppData\Roaming\QGIS\QGIS3\profiles')
    elif os == 'Linux':
        qgis_user_profile = Path('.local/share/QGIS/QGIS3/profiles')
    elif os == 'Darwin':  # MacOS?
        qgis_user_profile = Path('Library/Application Support/QGIS/QGIS3/profiles')
    else:
        raise NotImplemented('Could not detectect the OS system.')

    plugin_folder = Path(f'{profile}/python/plugins')
    res = Path(user_home_path / qgis_user_profile / plugin_folder).expanduser()

    return res
