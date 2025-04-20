import logging
import pathlib
import typing

from fspacker.exceptions import ProjectParseError
from fspacker.models import ProjectInfo

try:
    # Python 3.11+标准库
    import tomllib
except ImportError:
    # 兼容旧版本Python
    import tomli as tomllib


def parse_pyproject(project_dir: pathlib.Path = None) -> typing.Optional[ProjectInfo]:
    """
    解析项目目录下的 pyproject.toml 文件，获取项目信息

    :param project_dir: 项目目录路径
    :return: 项目信息对象
    :raises ProjectParseError: 如果项目路径无效或文件未找到
    """

    if not project_dir or not project_dir.exists():
        raise ProjectParseError("项目路径无效: [green underline]{project_dir}")

    config_path = project_dir / "pyproject.toml"
    if not config_path.is_file():
        raise ProjectParseError(f"路径下未找到 [red bold]pyproject.toml[/] 文件: [green underline]{project_dir}[/]")

    try:
        with config_path.open("rb") as f:
            data = tomllib.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"文件未找到: {config_path.resolve()}")  # noqa: B904
    except tomllib.TOMLDecodeError as e:
        raise RuntimeError(f"TOML解析错误: {e}")  # noqa: B904

    result = ProjectInfo()

    # PEP 621标准格式 (https://www.python.org/dev/peps/pep-0621/)
    if "project" in data:
        project = data["project"]
        result.name = project.get("name", "")
        if not result.name:
            raise ProjectParseError("未设置项目名称")

        result.dependencies = project.get("dependencies", [])

        # 处理可选依赖
        optional_deps = project.get("optional-dependencies", {})
        for group, deps in optional_deps.items():
            result.optional_dependencies[group] = deps

    # Poetry格式 (https://python-poetry.org/docs/pyproject/)
    elif "tool" in data and "poetry" in data["tool"]:
        poetry = data["tool"]["poetry"]
        result.dependencies = list(poetry.get("dependencies", {}).keys())

        # 移除python版本声明
        if "python" in result["dependencies"]:
            result.dependencies.remove("python")

        # 处理可选依赖组
        for group in poetry.get("group", {}).values():
            group_name = group.get("dependencies", {})
            result.optional_dependencies.update(group_name)

    logging.info(f"项目信息: {result}")
    return result
