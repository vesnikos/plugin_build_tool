from pathlib import Path
from typing import Union
from whichcraft import which


def file_changed(this: Union[str, Path], other: Union[str, Path]) -> bool:
    this_st_mtime = Path(this).stat().st_mtime
    other_st_mtime = Path(other).stat().st_mtime
    return this_st_mtime > other_st_mtime


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
