import pytest

from fspacker.exceptions import ProjectParseError
from fspacker.parsers.project import parse_pyproject


@pytest.mark.parametrize(
    "dirname, dependencies",
    [
        ("ex01_helloworld", ["defusedxml>=0.7.1", "orderedset>=2.0.3"]),
        ("ex02_office", ["pypdf>=5.4.0"]),
        ("ex03_tkinter", ["pyyaml>=6.0.2"]),
        ("ex04_pyside2", ["pyside2>=5.15.2.1"]),
        ("ex11_pygame", ["pygame>=2.6.1"]),
    ],
)
def test_parse_dependencies(dir_examples, dirname, dependencies):
    project_dir = dir_examples / dirname
    assert project_dir.exists()

    project_info = parse_pyproject(project_dir)
    assert project_info.name == dirname.replace("_", "-")
    assert project_info.dependencies == dependencies


def test_parse_project_info(dir_examples):
    dir_ex01 = dir_examples / "ex04_pyside2"
    assert dir_ex01.exists()

    project_info = parse_pyproject(dir_ex01)
    assert project_info.name == "ex04-pyside2"
    assert project_info.dependencies == [
        "pyside2>=5.15.2.1",
    ]
    assert project_info.contains_libname("pyside2")
    assert project_info.contains_libname("PySide2")
    assert not project_info.contains_libname("PyQt5")


def test_parse_pyproject_filenotfound(tmp_path):
    """测试当 pyproject.toml 文件未找到时，是否抛出 ProjectParseError 异常"""
    project_dir = tmp_path
    with pytest.raises(ProjectParseError) as excinfo:
        parse_pyproject(project_dir)
    assert "路径下未找到" in str(excinfo.value)


def test_parse_pyproject_toml_decode_error(tmp_path):
    """测试当 pyproject.toml 文件内容格式错误时，是否抛出 RuntimeError 异常"""
    project_dir = tmp_path
    toml_file = project_dir / "pyproject.toml"
    toml_file.write_text("invalid toml content")  # 写入无效的 TOML 格式内容
    with pytest.raises(Exception) as excinfo:
        parse_pyproject(project_dir)
    assert "TOML解析错误" in str(excinfo.value)
