import pathlib
import typing

from fspacker.exceptions import ProjectParseError

try:
    # Python 3.11+标准库
    import tomllib
except ImportError:
    # 兼容旧版本Python
    import tomli as tomllib

__all__ = [
    "ProjectInfo",
    "parse_pyproject",
]


class ProjectInfo:
    """项目构建信息"""

    # 窗口程序判定库
    _gui_libs = [
        "pyside2",
        "pyqt5",
        "pygame",
        "matplotlib",
        "tkinter",
        "pandas",
    ]

    def __init__(
        self,
        name: str = "",
        project_dir: pathlib.Path = None,
        dependencies: typing.Optional[typing.List[str]] = None,
        optional_dependencies: typing.Optional[typing.Dict[str, typing.List[str]]] = None,
    ):
        self.name = name
        self.project_dir = project_dir
        self.dependencies = dependencies or []
        self.optional_dependencies = optional_dependencies or {}

        # 解析数据
        self.data: typing.Optional[typing.Dict[str]] = None

    def __repr__(self):
        return f"依赖项: {self.dependencies}, 可选依赖项: {self.optional_dependencies}"

    def parse(self) -> None:
        """解析项目目录下的 pyproject.toml 文件，获取项目信息"""

        self._read_config()
        self._parse_dependencies()

    def contains_libname(self, lib_name: str) -> bool:
        """判断是否存在, 忽略大小写"""

        for dependency in self.dependencies:
            if lib_name.lower() in dependency.lower():
                return True

        return False

    @property
    def is_gui(self):
        """判断是否为 GUI 项目"""

        return any(self.contains_libname(lib) for lib in self._gui_libs)

    @property
    def normalized_name(self):
        """名称归一化，替换所有'-'为'_'"""
        return self.name.replace("-", "_")

    def _read_config(self) -> None:
        """读取配置文件"""
        if not self.project_dir or not self.project_dir.exists():
            raise ProjectParseError(f"项目路径无效: {self.project_dir}")

        config_path = self.project_dir / "pyproject.toml"

        if not config_path.is_file():
            raise ProjectParseError(f"路径下未找到 pyproject.toml 文件: {self.project_dir}")

        try:
            with config_path.open("rb") as f:
                self.data = tomllib.load(f)
        except FileNotFoundError as e:
            raise RuntimeError(f"文件未找到: {config_path.resolve()}") from e
        except tomllib.TOMLDecodeError as e:
            raise RuntimeError(f"TOML解析错误: {e}") from e
        except Exception as e:
            raise RuntimeError(f"未知错误: {e}") from e

    def _parse_dependencies(self) -> None:
        """解析依赖项"""
        if "project" in self.data:
            self._parse_pep621(self.data["project"])
        elif "tool" in self.data and "poetry" in self.data["tool"]:
            self._parse_poetry(self.data["tool"]["poetry"])
        else:
            raise ProjectParseError("不支持的 pyproject.toml 格式")

    def _parse_pep621(self, data: dict) -> None:
        """解析 PEP 621 格式的 pyproject.toml"""
        self.name = data.get("name", "")
        if not self.name:
            raise ProjectParseError("未设置项目名称")

        self.dependencies = data.get("dependencies", [])
        if not isinstance(self.dependencies, list):
            raise ProjectParseError(f"依赖项格式错误: {self.dependencies}")

        # 处理可选依赖项
        self.optional_dependencies = data.get("optional-dependencies", {})
        if not isinstance(self.optional_dependencies, dict):
            raise ProjectParseError(f"可选依赖项格式错误: {self.optional_dependencies}")

        # 解析可选依赖项
        self._parse_optional_dependencies()

    def _parse_optional_dependencies(self) -> None:
        """解析可选依赖项"""
        for group, deps in self.optional_dependencies.items():
            if isinstance(deps, str):
                self.optional_dependencies[group] = [deps]
            elif not isinstance(deps, list):
                raise ProjectParseError(f"可选依赖项格式错误: {group} -> {deps}")

        # 移除python版本声明
        if "python" in self.dependencies:
            self.dependencies.remove("python")

    def _parse_poetry(self, data: dict) -> None:
        """解析 Poetry 格式的 pyproject.toml"""
        self.name = data.get("name", "")
        if not self.name:
            raise ProjectParseError("未设置项目名称")

        # 处理依赖项
        dependencies = data.get("dependencies", {})
        if not isinstance(dependencies, dict):
            raise ProjectParseError(f"依赖项格式错误: {dependencies}")

        self.dependencies = list(dependencies.keys())

        # 处理可选依赖项
        optional_deps = data.get("group", {})
        if not isinstance(optional_deps, dict):
            raise ProjectParseError(f"可选依赖项格式错误: {optional_deps}")

        for group, deps in optional_deps.items():
            if isinstance(deps, dict):
                self.optional_dependencies[group] = list(deps.keys())
            else:
                raise ProjectParseError(f"可选依赖项格式错误: {group} -> {deps}")

        # 移除python版本声明
        if "python" in self.dependencies:
            self.dependencies.remove("python")


def parse_pyproject(project_dir: pathlib.Path) -> ProjectInfo:
    """解析项目目录下的 pyproject.toml 文件，获取项目信息"""

    project_info = ProjectInfo(project_dir=project_dir)
    project_info.parse()
    return project_info
