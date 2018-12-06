from typing import List, Union, Optional
from pathlib import Path
from configparser import ConfigParser

from pb_tool.utils import qgis_default_plugin_folder


class PbConf:

    def __init__(self, file_path: Union[str, Path]):
        self._file_path = Path(file_path)
        if not self._file_path.is_file():
            raise ValueError(f'{self._file_path.as_posix()} does not exist.')

        self._configuration = ConfigParser()
        self._configuration.read(self._file_path)
        if not self.is_valid:
            raise ValueError('The configuration file is not Valid')

    @property
    def file_path(self) -> Path:
        ret = Path(self._file_path)
        return ret

    @property
    def project_dir(self) -> Path:
        """ The project path, defined as where the configuration file is. """
        return Path(self.file_path).parent

    @property
    def plugin_name(self) -> str:
        name = self._configuration.get('plugin', 'name')

        return name

    @property
    def extra_files(self) -> List[Path]:

        # mandatory, at least two extra files should be present. (icon.png metadata.txt)
        # could be all files in a folder
        extra_files = []

        for entry in self._configuration.get('files', 'extra_files').split():
            entry = self.project_dir / Path(entry)
            if entry.is_dir():
                for _ in entry.glob('*.*'):
                    _ = _.relative_to(self.project_dir)
                    extra_files.append(_)
            else:
                entry = entry.relative_to(self.project_dir)
                extra_files.append(entry)

        return extra_files

    @property
    def python_files(self) -> List[Path]:
        """ A list of .py file to move with the plugin. Relative to 'project_dir'. """
        # mandatory, at least two extra files should be present. (icon.png metadata.txt)
        # could be all files in a folder

        python_files = []
        for entry in self._configuration.get('files', 'python_files').split():
            entry = self.project_dir / Path(entry)
            if entry.is_dir():
                for _ in entry.glob("*.py"):
                    _ = _.relative_to(self.project_dir)
                    python_files.append(_)
            else:
                entry = entry.relative_to(self.project_dir)
                python_files.append(entry)

        return python_files

    @property
    def ui_files(self) -> List[Path]:

        # mandatory, at least one ui file should be present

        ui_files = []
        for entry in self._configuration.get('files', 'ui_files').split():
            entry = self.project_dir / Path(entry)
            ui_files.append(entry)

        return ui_files

    @property
    def is_valid(self) -> bool:
        res = is_valid(self.file_path)
        return res

    @property
    def install_dir(self) -> Path:
        install_dir = self._configuration.get('plugin', 'install_dir') or None
        if install_dir is None:
            install_dir = qgis_default_plugin_folder

        install_dir = install_dir / self.plugin_name
        return install_dir

    @property
    def resource_files(self) -> List[Optional[Path]]:
        resource_files = self._configuration.get('files', 'resource_files').split()
        if len(resource_files) == 0:
            return []
        else:
            resource_files = map(Path, resource_files)
            resource_files = list(resource_files)

            return resource_files

    @classmethod
    def as_py(cls, plist: List[Path]) -> List[Path]:
        ret = []
        for p in plist:
            ret.append(p.with_suffix('.py'))

        return ret


def is_valid(conf: Union[Path, ConfigParser]) -> bool:
    """
    Check the pb_tool.cfg file for mandatory sections.
    """

    _configuration = None
    if isinstance(conf, Path):
        _configuration = ConfigParser().read(conf)
    if isinstance(conf, ConfigParser):
        _configuration = _configuration
    if _configuration is None:
        raise AttributeError('Conf must be either Configuration object or Path')

    # TODO:
    # Check if the plugin name has valid name.
    plugin_name = _configuration.get('plugin', 'name', fallback=None)
    if plugin_name is None:
        return False

    # Check if the files::python_files is set, and if they point to a valid file
    python_files = _configuration.get('files', 'python_files', fallback=None)
    if python_files is None:
        return False
    if _configuration.get('files', 'ui_files', fallback=None) is None:
        return False
    if _configuration.get('files', 'resource_files', fallback=None) is None:
        return False
    if _configuration.get('files', 'extra_files', fallback=None) is None:
        return False
    # Help dir should not be mandatory
    # if config.get('help', 'dir', fallback=None) is None:
    #     return False
    # if config.get('help', 'target', fallback=None) is None:
    #     return False

    return True
