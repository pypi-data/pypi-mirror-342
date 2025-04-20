import json
import pathlib

from fspacker.config import _save_json_config
from fspacker.config import get_cache_dir
from fspacker.config import get_libs_dir


def test_get_cache_dir_env_set(monkeypatch, tmp_path):
    """测试当 FSPACKER_CACHE 环境变量被设置时，get_cache_dir 返回正确路径"""

    monkeypatch.setenv("FSPACKER_CACHE", str(tmp_path))
    assert get_cache_dir() == tmp_path


def test_get_cache_dir_env_not_set(monkeypatch):
    """测试当 FSPACKER_CACHE 环境变量未设置时，get_cache_dir 返回默认路径"""

    monkeypatch.delenv("FSPACKER_CACHE", raising=False)
    expected_path = pathlib.Path("~").expanduser() / ".cache" / "fspacker"
    assert get_cache_dir() == expected_path


def test_get_libs_dir_env_set(monkeypatch, tmp_path):
    """测试当 FSPACKER_LIBS 环境变量被设置且路径存在时，get_libs_dir 返回正确路径"""

    monkeypatch.setenv("FSPACKER_LIBS", str(tmp_path))
    tmp_path.mkdir(exist_ok=True)
    assert get_libs_dir() == tmp_path


def test_get_libs_dir_env_not_set(monkeypatch):
    """测试当 FSPACKER_LIBS 环境变量未设置时，get_libs_dir 返回默认路径"""

    monkeypatch.delenv("FSPACKER_LIBS", raising=False)
    expected_path = get_cache_dir() / "libs-repo"
    assert get_libs_dir() == expected_path


def test_save_json_config(monkeypatch, tmp_path):
    """测试 _save_json_config 函数是否正确保存配置"""
    config_data = {"test_key": "test_value"}
    cache_dir = tmp_path
    monkeypatch.setattr("fspacker.config.get_cache_dir", lambda: cache_dir)
    monkeypatch.setattr("fspacker.config._config", config_data)

    config_file_path = cache_dir / "config.json"

    _save_json_config()

    with open(config_file_path) as f:
        saved_config = json.load(f)

    assert saved_config == config_data


def test_save_json_config_empty_config(monkeypatch, tmp_path):
    """测试当 _config 为空时，_save_json_config 函数不应保存任何内容"""
    cache_dir = tmp_path
    monkeypatch.setattr("fspacker.config.get_cache_dir", lambda: cache_dir)
    monkeypatch.setattr("fspacker.config._config", {})

    config_file_path = cache_dir / "config.json"

    _save_json_config()

    assert not config_file_path.exists()


def test_get_xxx_dir_creates_directory(monkeypatch, tmp_path):
    """测试当缓存目录不存在时，get_cache_dir 是否创建目录"""

    cache_dir = tmp_path / "nonexistent_cache"
    monkeypatch.setenv("FSPACKER_CACHE", str(cache_dir))

    assert not cache_dir.exists()
    get_cache_dir()
    assert cache_dir.exists()

    libs_dir = cache_dir / "libs-repo"
    monkeypatch.setenv("FSPACKER_LIBS", str(libs_dir))
    assert not libs_dir.exists()
    get_libs_dir()
    assert libs_dir.exists()
