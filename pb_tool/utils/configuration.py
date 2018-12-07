from configparser import ConfigParser
from pathlib import Path
from typing import List, Optional, Set, Union

from pb_tool.utils import qgis_default_plugin_folder


class PbConf:
    # Mandatory Fields
    _name: str = None
    _about: str = None
    _email: str = None
    _author: str = None
    _qgisMinimumVersion: str = None
    _description: str = None
    _version: float = None
    _tracker: str = None
    _repository: str = None

    _extra_files: set = set()
    _python_files: set = set()

    # optional
    _category: str = None
    _changelog: str = None
    _tag_list: List[str] = None
    _homepage: str = None
    _icon: str = None
    _experimental: bool = True

    # danger
    _deprecated: bool = False

    def __init__(self, pb_conf_fpath: Union[str, Path],
                 qgis_metadata_fpath: Union[str, Path]):
        self._configuration = ConfigParser()
        self.has_qgis_metadata = False

        self._file_path = Path(pb_conf_fpath)
        self._qgis_metadata_path = Path(qgis_metadata_fpath)

        if not self._file_path.is_file():
            raise ValueError(f'{self._file_path.as_posix()} does not exist.')
        self._configuration.read(self._file_path)

        if self._qgis_metadata_path.is_file():
            self._configuration.read(self._qgis_metadata_path)
            self.has_qgis_metadata = True

        if not self.is_valid:
            raise ValueError('The configuration file is not Valid')

    @property
    def about(self):
        res = self._configuration.get('general', 'about', fallback=None) or self._about
        return res

    @about.setter
    def about(self, value: str):
        value = value.strip()
        self._about = value

    @property
    def name(self) -> str:
        if self._name is None:
            self._name = self._configuration.get('general', 'name', fallback='') \
                         or self._configuration.get('plugin', 'name', fallback='')
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def email(self):
        if self._email is None:
            self._email = self._configuration.get('general', 'email', fallback='')
        return self._email

    @email.setter
    def email(self, value: str):
        value = value.strip()
        # TODO: valid the input email
        self._email = value

    @property
    def author(self):
        if self._author is None:
            self._author = self._configuration.get('general', 'author', fallback='')
        return self._author

    @author.setter
    def author(self, value: str):
        value = value.strip()
        self._author = value

    @property
    def qgisMinimumVersion(self):
        if self._qgisMinimumVersion is None:
            self._qgisMinimumVersion = self._configuration.get('general', 'qgisMinimumVersion', fallback='')
        return self._qgisMinimumVersion

    @qgisMinimumVersion.setter
    def qgisMinimumVersion(self, value: str):
        value = value.strip()
        self._qgisMinimumVersion = value

    @property
    def description(self):
        if self._description is None:
            self._description = self._configuration.get('general', 'description', fallback='')
        return self._description

    @description.setter
    def description(self, value: str):
        value = value.strip()
        self._description = value

    @property
    def plugin_version(self) -> Optional[float]:
        if self._version is None:
            self._version = self._configuration.getfloat('general', 'version', fallback=None)
        return self._version

    @plugin_version.setter
    def plugin_version(self, value: Union[float, str]):
        value = float(value)
        self._version = value

    @property
    def tracker(self):
        if self._tracker is None:
            self._tracker = self._configuration.get('general', 'tracker', fallback='')
        return self._tracker

    @tracker.setter
    def tracker(self, value: str):
        value = value.strip()
        self._tracker = value

    @property
    def repository(self):
        if self._repository is None:
            self._repository = self._configuration.get('general', 'repository', fallback='')
        return self._repository

    @repository.setter
    def repository(self, value: str):
        value = value.strip()
        self._repository = value

    @property
    def category(self):
        if self._category is None:
            self._category = self._configuration.get('general', 'category', fallback='')
        return self._category

    @category.setter
    def category(self, value: str):
        value = value.strip()
        self._category = value

    @property
    def changelog(self) -> str:
        if self._changelog is None:
            self._changelog = self._configuration.get('general', 'changelog', fallback='')
        return self._changelog

    @changelog.setter
    def changelog(self, value: str):
        value = value.strip()
        self._changelog = value

    @property
    def tag_list(self) -> List[str]:
        if self._tag_list is None:
            tag_list = self._configuration.get('general', 'tags', fallback='')
            tag_list = tag_list.split(',')
            self._tag_list = tag_list
        return self._tag_list

    @tag_list.setter
    def tag_list(self, value: List[str]):
        self._tag_list = value

    @property
    def homepage(self) -> str:
        if self._homepage is None:
            self._homepage = self._configuration.get('general', 'homepage', fallback='')
        return self._homepage

    @homepage.setter
    def homepage(self, value):
        self._homepage = value

    @property
    def icon(self):
        if self._icon is None:
            self._icon.get('general', 'icon', fallback='')
        return self._icon

    @icon.setter
    def icon(self, value):
        p = Path(value)
        if not p.is_file():
            raise AttributeError('%s is not an file.' % value)
        self._icon = value

    @property
    def experimental(self):
        return self._configuration.getboolean('general', 'experimental', fallback='') or self._experimental

    @experimental.setter
    def experimental(self, value: bool):
        self._experimental = bool(value)

    @property
    def deprecated(self):
        return self._configuration.getboolean('general', 'deprecated', fallback=False) or self._deprecated

    @deprecated.setter
    def deprecated(self, value: bool):
        self._deprecated = bool(value)

    @property
    def is_valid(self) -> bool:
        """
            Check if the configuration is valid.
        """

        def nop(val) -> bool:
            if val is None:
                return True
            if val is '':
                return True

        missing = []
        # Mandatory Fields from metadata.txt
        if nop(self.name):
            missing.append('name')
        if nop(self.about):
            missing.append('about')
        if nop(self.email):
            missing.append('email')
        if nop(self.author):
            missing.append('author')
        if nop(self.qgisMinimumVersion):
            missing.append('qgisMinimumVersion')
        if nop(self.description):
            missing.append('description')
        if nop(self.plugin_version):
            missing.append('description')
        if nop(self.tracker):
            missing.append('tracker')
        if nop(self.repository):
            missing.append('repository')

        # mandatory files from pb_tool.cfg
        if nop(self.ui_files):
            missing.append('ui_files')
        if nop(self.python_files):
            missing.append('python_files')

        if len(missing) == 0:
            return True
        else:
            # check missing list for which one were not set
            return False

    # @property
    # def file_path(self) -> Path:
    #     """ The path for the pb_tool.cfg file """
    #     ret = Path(self._file_path)
    #     return ret

    @property
    def project_dir(self) -> Path:
        """ The project path, defined as where the configuration file is. """
        return Path(self._file_path).parent

    @property
    def plugin_name(self) -> str:
        # name = self._configuration.get('plugin', 'name'
        # deprecated; use self.name

        return self.name

    @property
    def extra_files(self) -> Set[Path]:
        for entry in self._configuration.get('files', 'extra_files').split():
            entry = self.project_dir / Path(entry)
            if entry.is_dir():
                for _ in entry.glob('*.*'):
                    _ = _.relative_to(self.project_dir)
                    self._extra_files.add(_)
            else:
                entry = entry.relative_to(self.project_dir)
                self._extra_files.add(entry)

        return self._extra_files

    @property
    def python_files(self) -> Set[Path]:
        """ A list of .py file to move with the plugin. Relative to 'project_dir'. """
        # mandatory, at least two extra files should be present.
        # could be all files in a folder

        for entry in self._configuration.get('files', 'python_files').split():
            entry = self.project_dir / Path(entry)
            if entry.is_dir():
                for _ in entry.glob("*.py"):
                    _ = _.relative_to(self.project_dir)
                    self._python_files.add(_)
            else:
                entry = entry.relative_to(self.project_dir)
                self._python_files.add(entry)

        return self._python_files

    @property
    def ui_files(self) -> List[Path]:

        # mandatory, at least one ui file should be present

        ui_files = []
        for entry in self._configuration.get('files', 'ui_files').split():
            entry = self.project_dir / Path(entry)
            ui_files.append(entry)

        return ui_files

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
