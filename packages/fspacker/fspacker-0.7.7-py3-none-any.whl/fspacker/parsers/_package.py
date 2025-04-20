import email.message
import pathlib
import tarfile
import typing
import zipfile
from pathlib import Path

from packaging.requirements import Requirement

from fspacker.utils.requirement import RequirementParser

__all__ = ["analyze_package_deps"]


class PackageFileDependencyAnalyzer:
    @staticmethod
    def extract_metadata(package_path: Path) -> typing.Optional[email.message.Message]:
        """从包文件中提取元数据"""
        if package_path.suffix == ".whl":
            with zipfile.ZipFile(package_path) as z:
                for name in z.namelist():
                    if name.endswith(".dist-info/METADATA"):
                        metadata = z.read(name).decode("utf-8")
                        return email.message_from_string(metadata)

        elif package_path.suffix in (".tar.gz", ".zip"):
            opener = tarfile.open if package_path.suffix == ".gz" else zipfile.ZipFile
            with opener(package_path) as archive:
                for member in archive.getmembers():
                    if member.name.endswith(("PKG-INFO", "METADATA")):
                        fileobj = archive.extractfile(member)
                        metadata = fileobj.read().decode("utf-8")
                        return email.message_from_string(metadata)
        return None

    @classmethod
    def analyze_dependencies(cls, package_path: Path) -> typing.List[Requirement]:
        metadata = cls.extract_metadata(package_path)
        if not metadata:
            return []

        requirements = []
        for field in ["Requires-Dist", "Requires"]:
            for req_str in metadata.get_all(field, []):
                req = RequirementParser.parse_requirement(req_str)
                if req:
                    requirements.append(req)
        return requirements

    @classmethod
    def analyze_to_list(cls, package_path: Path) -> typing.List[Requirement]:
        """返回Requirement对象列表（去重）"""
        return list(cls.analyze_dependencies(package_path).values())


__analyzer = PackageFileDependencyAnalyzer()


def analyze_package_deps(package_file_path: pathlib.Path):
    global __analyzer

    return __analyzer.analyze_dependencies(package_file_path)
