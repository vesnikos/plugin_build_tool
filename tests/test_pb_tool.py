import platform
from pathlib import Path
import pytest

TESTS_DIR = Path(__file__).parent


@pytest.fixture
def valid_conf_file():
    ret = TESTS_DIR / 'sample1' / 'pb_tool.cfg'
    ret = ret.as_posix()
    return ret


def test_conf_is_valid(valid_conf_file):

    # PbConf.is_valid tests if configuration is valid

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


def test_cong_get_ui_files(valid_conf_file):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(valid_conf_file)

    res = config.ui_files
    assert res == [Path('main_window.ui'), Path('ui/about.ui')]


def test_cong_get_ui_files_as_py(valid_conf_file):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(valid_conf_file)

    res = config.as_py(config.ui_files)
    assert res == [Path('main_window.py'), Path('ui/about.py')]


def test_conf_get_extra_files(valid_conf_file):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(valid_conf_file)

    assert config.extra_files


def test_conf_get_resource_files(valid_conf_file):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(valid_conf_file)

    assert config.resource_files == [Path('resources.qrc'), ]


def test_conf_get_plugin_name(valid_conf_file):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(valid_conf_file)

    assert config.plugin_name == 'TestPlugin'


@pytest.mark.skipif(platform.system() != 'Windows',
                    reason="Non Windows Tests missing.")
def test_conf_get_install_dir(valid_conf_file):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(valid_conf_file)
    left = config.install_dir

    os = platform.system()
    if os == 'Windows':
        right = Path(r'~/AppData\Roaming\QGIS\QGIS3\profiles/default/python/plugins/TestPlugin').expanduser()
        assert left == right
    # elif os == 'Linux':
    #     qgis_user_profile = user_home_path / Path('.local/share/QGIS/QGIS3/profiles')
    # elif os == 'Darwin':  # MacOS?
    #     qgis_user_profile = user_home_path / Path('Library/Application Support/QGIS/QGIS3/profiles')


def test_conf_path_list_as_py():
    from pb_tool.utils.configuration import PbConf

    plist = [Path('asdf.qrc'), ]
    result = PbConf.as_py(plist)

    assert result == [Path('asdf.py'), ]
