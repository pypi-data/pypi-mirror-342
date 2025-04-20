"""本模块包含库所需常用函数"""

import logging
import re
import typing
from typing import Optional

from packaging import requirements
from packaging.requirements import InvalidRequirement
from packaging.requirements import Requirement


class RequirementParser:
    @staticmethod
    def normalize_requirement_string(req_str: str) -> Optional[str]:
        """
        规范化需求字符串，处理以下特殊情况：
        1. 括号包裹的版本：shiboken2 (==5.15.2.1) -> shiboken2==5.15.2.1
        2. 不规范的版本分隔符：package@1.0 -> package==1.0
        3. 移除多余空格和注释
        """
        # 移除注释和首尾空格
        req_str = re.sub(r"#.*$", "", req_str).strip()
        if not req_str:
            return None

        # 处理括号包裹的版本 (常见于PySide生态)
        if "(" in req_str and ")" in req_str:
            req_str = re.sub(r"$([^)]+)$", r"\1", req_str)

        # 替换不规范的版本分隔符
        req_str = re.sub(r"([a-zA-Z0-9_-]+)@([0-9.]+)", r"\1==\2", req_str)

        # 标准化版本运算符（处理 ~= 和意外的空格）
        req_str = re.sub(r"~=\s*", "~=", req_str)
        req_str = re.sub(r"([=<>!~]+)\s*", r"\1", req_str)

        # 标准化版本运算符（处理 ; 以后的内容）
        req_str = re.sub(r" ; .*", "", req_str)

        return req_str.strip()

    @classmethod
    def parse_requirement(cls, req_str: str) -> Optional[Requirement]:
        """安全解析需求字符串为Requirement对象"""
        normalized = cls.normalize_requirement_string(req_str)
        if not normalized:
            return None

        try:
            # 分离环境标记
            if ";" in normalized:
                req_part, marker = normalized.split(";", 1)
                req = Requirement(req_part.strip())
                req.marker = marker.strip()
            else:
                req = Requirement(normalized)
            return req
        except InvalidRequirement as e:
            print(f"⚠  Failed to parse '{req_str}': {str(e)}")
            return None


def parse_requirement(req_str: str) -> typing.Optional[requirements.Requirement]:
    """解析需求字符串为Requirement对象"""

    try:
        return requirements.Requirement(req_str)
    except requirements.InvalidRequirement:
        logging.error(f"非法 requirement: {req_str}")
        return None
