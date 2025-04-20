from fspacker.packers.factory import PackerFactory


class BasePacker:
    """针对特定场景打包工具"""

    NAME = "基础打包"

    def __init__(self, parent: PackerFactory):
        self.parent = parent

    def __repr__(self):
        return f"调用 [[green]{self.NAME} - {self.__class__.__name__}[/]] 打包工具"

    @property
    def root_dir(self):
        return self.parent.root_dir

    @property
    def dest_dir(self):
        return self.parent.dest_dir

    @property
    def mode(self):
        return self.parent.mode

    @property
    def project_info(self):
        return self.parent.project_info

    @property
    def dependencies(self):
        return self.project_info.dependencies

    def pack(self): ...
