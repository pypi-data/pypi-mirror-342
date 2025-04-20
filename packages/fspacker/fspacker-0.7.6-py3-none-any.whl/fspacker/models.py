"""定义库所需基础类"""

import dataclasses
import typing


@dataclasses.dataclass
class PackMode:
    """打包模式"""

    MODES = dict(
        archive=("", "压缩"),
        rebuild=("", "重构"),
        debug=("非调试", "调试"),
        offline=("在线", "离线"),
        simplify=("", "简化"),
        use_tk=("", "tk"),
    )

    archive: bool = False  # 压缩包模式
    rebuild: bool = False  # 重构模式
    debug: bool = False  # 调试模式，显示打包时间等信息
    offline: bool = False  # 离线模式
    simplify: bool = False  # 简化模式, 加速pyside等库打包速度
    use_tk: bool = False  # 启用 tk 打包

    def __repr__(self):
        """显示模式信息"""

        mode_str = []
        for k, v in self.__dict__.items():
            prefix = "[red bold]" if int(v) else "[green bold]"
            val = self.MODES.get(k)[int(v)]
            if val:
                mode_str.append(prefix + val + "[/]")

        return f"模式: [{', '.join(mode_str)}]"


@dataclasses.dataclass
class ProjectInfo:
    """依赖项信息"""

    # 窗口程序判定库
    _gui_libs = [
        "pyside2",
        "pyqt5",
        "pygame",
        "matplotlib",
        "tkinter",
        "pandas",
    ]

    name: str = ""
    dependencies: typing.Optional[typing.List[str]] = None
    optional_dependencies: typing.Optional[typing.Dict[str, typing.List[str]]] = None

    def __repr__(self):
        return f"依赖项: {self.dependencies}, 可选依赖项: {self.optional_dependencies}"

    def contains_libname(self, lib_name: str) -> bool:
        """判断是否存在, 忽略大小写"""

        for dependency in self.dependencies:
            if lib_name.lower() in dependency.lower():
                return True

        return False

    def is_gui_project(self):
        """判断是否为 GUI 项目"""

        return any(self.contains_libname(lib) for lib in self._gui_libs)

    @property
    def normalized_name(self):
        """名称归一化，替换所有'-'为'_'"""
        return self.name.replace("-", "_")
