import logging
import shutil

from fspacker.packers._base import BasePacker


class PostPacker(BasePacker):
    NAME = "项目后处理打包"

    def pack(self):
        if self.mode.archive:
            logging.info(f"压缩文件: [[green]{self.dest_dir}[/]]")
            try:
                shutil.make_archive(
                    self.dest_dir.name,
                    "zip",
                    self.dest_dir.parent,
                    self.dest_dir.name,
                )
            except OSError as e:
                logging.info(f"压缩失败: [red bold]{e}")
