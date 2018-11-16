from warnings import warn
from typing import Union
from pathlib import Path


def qgis_plugin_dir()->Union[Path,None]:

    try:
        from PyQt5.QtCore import QStandardPaths, QDir
        path = QStandardPaths.standardLocations(QStandardPaths.AppDataLocation)[0]
        plugin_path = Path(QDir.homePath(), path, 'QGIS/QGIS3/profiles/default/python/plugins')
    except ImportError:
        warn('this python enviroment was not able to import the PyQt module and extract the QGIS path')
        return None

    return plugin_path
