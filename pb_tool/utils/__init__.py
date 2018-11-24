import platform

from pathlib import Path

from .find_qgis_dir import qgis_plugin_dir

__all__ = [ 'qgis_plugin_dir', 'qgis_dst_plugin_folder']


def qgis_dst_plugin_folder(profile='default') -> Path:
    """ The QGIS master Plugin folder """

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
