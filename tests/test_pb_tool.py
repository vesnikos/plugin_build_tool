from pathlib import Path
import pytest

TESTS_DIR = Path(__file__).parent


@pytest.fixture
def valid_conf_file():
    ret = TESTS_DIR / 'sample1' / 'pb_tool.cfg'
    ret = ret.as_posix()
    return ret


def test_conf_is_valid(valid_conf_file):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(valid_conf_file)

    assert config.is_valid is True


def test_conf_get_py_files(valid_conf_file):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(valid_conf_file)

    res = config.python_files
    assert res == [Path('__init__.py'),
                   Path('test_plugin.py'),
                   Path('test_plugin_dialog.py'),
                   Path('folder1/file.py'),
                   Path('folder1/subfolder1/file.py'),
                   Path('folder1/subfolder1/file2.py')]


def test_conf_get_extra_files(valid_conf_file):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(valid_conf_file)

    assert config.extra_files


def test_conf_get_main_dialog(valid_conf_file):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(valid_conf_file)

    assert config.main_dialog
