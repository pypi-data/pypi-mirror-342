import atexit
import json
import os
import pathlib
import platform
import typing

# 常量定义
PYTHON_VER = platform.python_version()
PYTHON_VER_SHORT = ".".join(PYTHON_VER.split(".")[:2])
PYTHON_EXE = "python.exe" if platform.system() == "Windows" else "python3"
MACHINE_CODE = platform.machine().lower()

# python 镜像
EMBED_URL_PREFIX: typing.Dict[str, str] = dict(
    official="https://www.python.org/ftp/python/",
    huawei="https://mirrors.huaweicloud.com/python/",
)
# pip 镜像
PIP_URL_PREFIX: typing.Dict[str, str] = dict(
    aliyun="https://mirrors.aliyun.com/pypi/simple/",
    tsinghua="https://pypi.tuna.tsinghua.edu.cn/simple/",
    ustc="https://pypi.mirrors.ustc.edu.cn/simple/",
    huawei="https://mirrors.huaweicloud.com/repository/pypi/simple/",
)

# 路径定义
DIR_SRC = pathlib.Path(__file__).parent
DIR_ASSETS = DIR_SRC / "assets"


def get_cache_dir() -> pathlib.Path:
    """缓存目录, 默认在 User/.cache/fspacker 路径下"""

    cache_env = os.getenv("FSPACKER_CACHE")
    if cache_env is not None:
        cache_dir = pathlib.Path(cache_env)
    else:
        cache_dir = pathlib.Path("~").expanduser() / ".cache" / "fspacker"

    if not cache_dir.exists():
        cache_dir.mkdir(exist_ok=True, parents=True)

    return cache_dir


def get_libs_dir() -> pathlib.Path:
    """库目录, 默认在 User/.cache/fspacker/libs-repo 路径下"""

    cache_env = os.getenv("FSPACKER_LIBS")
    if cache_env is not None and (cache_path := pathlib.Path(cache_env)).exists():
        libs_dir = cache_path
    else:
        libs_dir = get_cache_dir() / "libs-repo"

    if not libs_dir.exists():
        libs_dir.mkdir(exist_ok=True, parents=True)

    return libs_dir


_config: typing.Dict[str, typing.Any] = {}


def get_json_config() -> typing.Dict[str, typing.Any]:
    global _config

    if not len(_config):
        config_file = get_cache_dir() / "config.json"
        if config_file.exists():
            with open(config_file) as file:
                _config = json.load(file)

    return _config


def _save_json_config() -> None:
    """Save config file while exiting."""
    global _config

    if len(_config):
        config_file = get_cache_dir() / "config.json"
        with open(config_file, "w") as file:
            json.dump(_config, file, indent=4, ensure_ascii=True, check_circular=True)


atexit.register(_save_json_config)
