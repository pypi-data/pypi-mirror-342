import logging
import shutil

from fspacker.packers._base import BasePacker


class PrePacker(BasePacker):
    NAME = "项目初始化打包"

    def pack(self):
        if self.mode.rebuild:
            logging.info(f"清理旧文件: [[green]{self.dest_dir}[/]]")
            try:
                shutil.rmtree(self.dest_dir, ignore_errors=True)
            except OSError as e:
                logging.info(f"清理失败: [red bold]{e}")

        for directory in (self.dest_dir,):
            logging.info(f"创建文件夹: [[purple]{directory.name}[/]]")
            directory.mkdir(parents=True, exist_ok=True)
