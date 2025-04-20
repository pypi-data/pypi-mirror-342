import logging
import shutil

from fspacker import config
from fspacker.packers._base import BasePacker


class BuiltInLibPacker(BasePacker):
    NAME = "内置依赖库打包"

    def pack(self):
        if self.mode.use_tk:
            tk_lib = config.DIR_ASSETS / "tkinter-lib.zip"
            tk_package = config.DIR_ASSETS / "tkinter.zip"
            logging.info(f"解压tk文件: [green]{tk_lib}[/], [green]{tk_package}")
            shutil.unpack_archive(tk_lib, self.dest_dir, "zip")
            shutil.unpack_archive(tk_package, self.dest_dir / "site-packages", "zip")
