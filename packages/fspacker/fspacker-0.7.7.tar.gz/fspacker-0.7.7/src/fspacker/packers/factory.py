import logging
import pathlib
import time
import typing

__all__ = ["pack"]


from fspacker.parsers.mode import PackMode


class PackerFactory:
    """打包工具"""

    def __init__(
        self,
        root_dir: pathlib.Path,
        dest_dir: pathlib.Path,
        mode: PackMode,
    ):
        from fspacker.packers._builtins import BuiltInLibPacker
        from fspacker.packers._entry import EntryPacker
        from fspacker.packers._library import LibraryPacker
        from fspacker.packers._post import PostPacker
        from fspacker.packers._pre import PrePacker
        from fspacker.packers._runtime import RuntimePacker
        from fspacker.packers._source import SourceResPacker
        from fspacker.parsers.project import parse_pyproject

        self.mode = mode

        self.root_dir = root_dir
        self.dest_dir = dest_dir
        self.project_info = parse_pyproject(root_dir)

        # 打包器集合, 注意打包顺序
        self.spec_packers: typing.Dict[str, typing.Any] = dict(
            project_folder=PrePacker(self),
            source_res=SourceResPacker(self),
            library=LibraryPacker(self),
            builtin=BuiltInLibPacker(self),
            exe_entry=EntryPacker(self),
            runtime=RuntimePacker(self),
            post=PostPacker(self),
        )

    def pack(self):
        from fspacker.exceptions import ProjectParseError

        if not self.project_info:
            raise ProjectParseError("项目信息无效")

        logging.info(f"启动构建, 源码根目录: [[green underline]{self.root_dir}[/]]")
        if not self.root_dir.exists():
            raise ProjectParseError(f"目录路径不存在: [bold red]{self.root_dir}")

        t0 = time.perf_counter()

        for _, spec_packer in self.spec_packers.items():
            logging.info(spec_packer)
            spec_packer.pack()

        logging.info(f"打包完成! 总用时: [{time.perf_counter() - t0:.4f}]s.")


def pack(
    root_dir: pathlib.Path,
    dest_dir: pathlib.Path,
    mode: PackMode,
) -> None:
    """打包工具入口"""
    factory = PackerFactory(root_dir, dest_dir, mode)
    factory.pack()
