import logging
import shutil
import string

from fspacker import config
from fspacker.packers._base import BasePacker

# int file template
INT_TEMPLATE = string.Template(
    """\
import sys, os
sys.path.append(os.path.join(os.getcwd(), "src"))
from $SRC import main
main()
"""
)

INT_TEMPLATE_QT = string.Template(
    """\
import sys, os
import $LIB_NAME

qt_dir = os.path.dirname($LIB_NAME.__file__)
plugin_path = os.path.join(qt_dir, "plugins" , "platforms")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path
sys.path.append(os.path.join(os.getcwd(), "src"))
from $SRC import main
main()
"""
)


class EntryPacker(BasePacker):
    NAME = "入口程序打包"

    def pack(self):
        name = self.project_info.normalized_name

        exe_filename = "gui.exe" if self.project_info.is_gui else "console.exe"
        src_exe_path = config.DIR_ASSETS / exe_filename
        dst_exe_path = self.dest_dir / f"{name}.exe"

        logging.info(f"打包目标类型: {'[green bold]窗口' if self.project_info.is_gui else '[red bold]控制台'}[/]")
        logging.info(
            f"复制可执行文件: [green underline]{src_exe_path.name} -> "
            f"{dst_exe_path.relative_to(self.root_dir)}[/] [bold green]:heavy_check_mark:"
        )
        shutil.copy(src_exe_path, dst_exe_path)

        dst_int_path = self.dest_dir / f"{name}.int"

        logging.info(
            f"创建 int 文件: [green underline]{name}.int -> {dst_int_path.relative_to(self.root_dir)}"
            f"[/] [bold green]:heavy_check_mark:"
        )

        for lib_name in ["PySide2", "PyQt5", "PySide6", "PyQt6"]:
            if self.project_info.contains_libname(lib_name):
                content = INT_TEMPLATE_QT.substitute(SRC=f"src.{name}", LIB_NAME=lib_name)
                break
        else:
            content = INT_TEMPLATE.substitute(SRC=f"src.{name}")

        with open(dst_int_path, "w") as f:
            f.write(content)
