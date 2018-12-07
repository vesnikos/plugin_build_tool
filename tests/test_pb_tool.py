import platform
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).parent


@pytest.fixture
def conf():
    ret = TESTS_DIR / 'sample2' / 'pb_tool.cfg'
    ret = ret.as_posix()
    return ret


@pytest.fixture
def metadata():
    ret = TESTS_DIR / 'sample2' / 'metadata.txt'
    ret = ret.as_posix()
    return ret


def test_pb_conf_attributes(conf, metadata):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(conf, metadata)
    assert config.about == 'A paragraph contained a detailed description. No Html.'
    assert config.author == 'Just Me'
    assert config.changelog == 'Changes:\n1.0 - First Release\n0.9.1 - Bug fix.\n0.9.0 - Last Feature Before Release'
    assert config.deprecated is False
    assert config.description == 'A multiline example\ndescription of what this plugin\nis about. No HTML.'
    assert config.email == 'me@example.com'
    assert config.experimental is True
    # separate bellow
    # assert config.extra_files
    assert config.has_qgis_metadata is True
    assert config.homepage == 'http://...'
    # separate bellow
    # assert config.install_dir
    assert config.is_valid is True
    assert config.name == 'HelloWorld'
    assert config.plugin_name == 'HelloWorld'
    # separate bellow
    # assert config.project_dir
    # separate bellow
    # assert config.python_files
    assert config.qgisMinimumVersion == '3.4'
    assert config.repository == 'http://...'
    # separate bellow
    # assert config.resource_files
    assert config.tag_list == ['raster', 'hello-world', 'python']
    assert config.tracker == 'http://...'
    # separate bellow
    # assert config.ui_files
    assert config.plugin_version == 0.1


def test_conf_is_valid(conf, metadata):
    # PbConf.is_valid tests if configuration is valid

    from pb_tool.utils.configuration import PbConf
    config = PbConf(conf, metadata)

    assert config.is_valid is True


def test_conf_get_project_dir(conf, metadata):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(conf, metadata)

    project_path = config.project_dir
    expected_path = Path(conf, metadata).parent

    assert project_path == expected_path


@pytest.mark.skip()
def test_conf_get_py_files(conf, metadata):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(conf, metadata)

    res = config.python_files
    assert res == [Path('__init__.py'),
                   Path('test_plugin.py'),
                   Path('test_plugin_dialog.py'),
                   Path('folder1/file.py'),
                   Path('folder1/subfolder1/file.py'),
                   Path('folder1/subfolder1/file2.py')]


def test_cong_get_ui_files(conf, metadata):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(conf, metadata)

    result = config.ui_files
    expected = [config.project_dir / Path('main_window.ui'),
                config.project_dir / Path('ui/about.ui')]

    assert result == expected


def test_cong_get_ui_files_as_py(conf, metadata):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(conf, metadata)

    ui_files = config.ui_files
    result = config.as_py(ui_files)
    expected = [config.project_dir / Path('main_window.py'),
                config.project_dir / Path('ui/about.py')]
    assert result == expected


def test_conf_get_extra_files(conf, metadata):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(conf, metadata)

    assert config.extra_files


def test_conf_get_resource_files(conf, metadata):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(conf, metadata)

    assert config.resource_files == [Path('resources.qrc'), ]


@pytest.mark.skipif(platform.system() != 'Windows',
                    reason="Non Windows Tests missing.")
def test_conf_get_install_dir(conf, metadata):
    from pb_tool.utils.configuration import PbConf
    config = PbConf(conf, metadata)
    left = config.install_dir

    os = platform.system()
    if os == 'Windows':
        right = Path(r'~/AppData\Roaming\QGIS\QGIS3\profiles/default/python/plugins/HelloWorld').expanduser()
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


def test_files_compile_ui(conf, metadata):
    from pb_tool.utils.files import compile_ui

    from pb_tool.utils.configuration import PbConf
    config = PbConf(conf, metadata)
    correct_ui, broken_ui_file = config.ui_files
    result = compile_ui(correct_ui)

    assert result == correct_ui.with_suffix('.py')
    # this one raises ValueError
    with pytest.raises(ValueError):
        compile_ui(broken_ui_file)

# def test_files_clean_ui_files(conf, metadata):
#     from pb_tool.utils.files import compile_ui
