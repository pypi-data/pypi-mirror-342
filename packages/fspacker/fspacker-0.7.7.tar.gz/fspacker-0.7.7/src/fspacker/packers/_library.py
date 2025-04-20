import logging
import re
import typing

from packaging.requirements import Requirement

from fspacker import config
from fspacker.packers._base import BasePacker
from fspacker.parsers._package import analyze_package_deps
from fspacker.utils.package import download_to_libs_dir
from fspacker.utils.package import get_cached_package
from fspacker.utils.package import install_package
from fspacker.utils.requirement import parse_requirement


class LibraryPacker(BasePacker):
    NAME = "依赖库打包"

    def _install_lib(self, req: Requirement):
        dest_dir = self.dest_dir / "site-packages"
        dest_dir.mkdir(parents=True, exist_ok=True)

        lib_folder = dest_dir / req.name
        if lib_folder.exists():
            logging.info(f"依赖库 [[red]{req.name}[/]] 已存在, 跳过")
            return None

        logging.info(f"打包依赖: [[green bold]{req}[/]]")
        cached_file = get_cached_package(req)
        if cached_file:
            logging.info(f"找到本地满足要求的依赖: [[green]{cached_file.name}]")
        else:
            logging.info(f"下载依赖: [[green]{req}[/]]")
            cached_file = download_to_libs_dir(req)

        if cached_file.is_file():
            logging.info(f"安装依赖: [[green]{cached_file.name}[/]]")
            install_package(req, cached_file, dest_dir, simplify=self.parent.mode.simplify)
            return cached_file
        else:
            logging.error(f"处理依赖失败: [[red bold]{req}[/]]")
            return None

    def pack(self):
        req_libs = self.dependencies
        logging.info(f"分析一级依赖库: [[green bold]{req_libs}[/]]")
        for req_lib in req_libs:
            req = parse_requirement(req_lib)
            logging.info(f"打包顶层依赖: [[green bold]{req}[/]]")

            cached_file = self._install_lib(req)
            if cached_file:
                secondary_reqs = analyze_package_deps(cached_file)
                logging.info(f"分析二级依赖: [[green]{secondary_reqs}[/]]")
                for secondary_req in secondary_reqs:
                    self._install_lib(secondary_req)

    @staticmethod
    def normalize_package_name(dep_requirement: str) -> typing.Tuple[str, str]:
        """标准化包名，去除版本约束，返回名称和版本"""

        name, version = re.split(r"[><=!~]", dep_requirement)
        return name.strip(), version.strip()

    @staticmethod
    def is_cached(package_req: str) -> bool:
        """检查包是否已存在于缓存"""
        package_name, package_ver = LibraryPacker.normalize_package_name(package_req)

        return any(
            pkg.name.startswith(f"{package_name}-") and pkg.suffix in (".whl", ".tar.gz", ".zip")
            for pkg in config.get_cache_dir().glob(f"{package_name}-{package_ver}")
        )
