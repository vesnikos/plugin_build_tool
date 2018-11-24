from typing import List, Union
from pathlib import Path
from configparser import ConfigParser
import glob


class PbConf:

    def __init__(self, file_path: Union[str, Path]):
        self._file_path = Path(file_path)
        if not self._file_path.is_file():
            raise ValueError(f'{self._file_path.as_posix()} does not exist.')

        self._configuration = ConfigParser()
        self._configuration.read(self._file_path)

    @property
    def file_path(self)->Path:
        ret = Path(self._file_path)
        return ret

    @property
    def project_dir(self) -> Path:
        ''' The project path, defined as where the configuration file is. '''
        return Path(self.file_path).parent

    @property
    def main_dialog(self) -> List[Path]:
        main_dialog = self.configuration.get('files', 'main_dialog').split()

        main_dialog = map(Path, main_dialog)
        return main_dialog

    @property
    def extra_files(self) -> List[Path]:

        # this is not mandatory
        f = self.configuration.get('files', 'extra_files', fallback='').split()

        f = map(Path, f)
        return f

    @property
    def python_files(self) -> List[Path]:

        ''' A list of .py file to move with the plugin. Relative to 'project_dir'. '''

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
    def is_valid(self) -> bool:
        """
        Check the pb_tool.cfg file for mandatory sections.
        """

        plugin_name = self._configuration.get('plugin', 'name', fallback=None)
        if plugin_name is None:
            return False

        # Check if the files::python_files is set, and if they point to a valid file
        python_files = self._configuration.get('files', 'python_files', fallback=None)
        if python_files is None:
            return False
        if self._configuration.get('files', 'main_dialog', fallback=None) is None:
            return False
        if self._configuration.get('files', 'resource_files', fallback=None) is None:
            return False
        if self._configuration.get('files', 'extras', fallback=None) is None:
            return False
        # Help dir should not be mandatory
        # if config.get('help', 'dir', fallback=None) is None:
        #     return False
        # if config.get('help', 'target', fallback=None) is None:
        #     return False

        return True
