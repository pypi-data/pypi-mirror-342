import logging
import pathlib
import shutil

import typer

from fspacker.packers._base import BasePacker


class SourceResPacker(BasePacker):
    NAME = "源码 & 资源打包"

    # 忽视清单
    IGNORE_ENTRIES = ["dist-info", "__pycache__", "site-packages", "runtime", "dist", ".venv"]

    def _valid_file(self, filepath: pathlib.Path) -> bool:
        return all(x not in str(filepath) for x in self.IGNORE_ENTRIES)

    def pack(self):
        dest_dir = self.dest_dir / "src"
        source_files = list(file for file in self.root_dir.rglob("*.py") if self._valid_file(file))

        for source_file in source_files:
            with open(source_file, encoding="utf8") as f:
                content = "\n".join(f.readlines())
            if "def main():" in content:
                source_folder = source_file.absolute().parent
                break
        else:
            logging.error("未找到入口 Python 文件, 退出")
            typer.Exit(code=2)

        dest_dir.mkdir(parents=True, exist_ok=True)
        for entry in source_folder.iterdir():
            dest_path = dest_dir / entry.name

            if entry.is_file():
                logging.info(f"复制目标文件: [green underline]{entry.name}[/] [bold green]:heavy_check_mark:")
                shutil.copy2(entry, dest_path)
            elif entry.is_dir():
                if entry.stem not in self.IGNORE_ENTRIES:
                    logging.info(f"复制目标文件夹: [purple underline]{entry.name}[/] [bold purple]:heavy_check_mark:")
                    shutil.copytree(entry, dest_path, dirs_exist_ok=True)
                else:
                    logging.info(f"目标文件夹 [red]{entry.name}[/] 已存在, 跳过")
