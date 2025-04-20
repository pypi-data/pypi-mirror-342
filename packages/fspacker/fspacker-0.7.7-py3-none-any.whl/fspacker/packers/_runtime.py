import logging
import shutil
import time

import typer

from fspacker import config
from fspacker.packers._base import BasePacker
from fspacker.utils.checksum import calc_checksum
from fspacker.utils.url import get_fastest_url
from fspacker.utils.url import safe_read_url_data


class RuntimePacker(BasePacker):
    NAME = "运行时打包"
    EMBED_DIR = config.get_cache_dir() / "embed-repo"
    EMBED_FILE_NAME = f"python-{config.PYTHON_VER}-embed-{config.MACHINE_CODE}.zip"
    EMBED_FILEPATH = EMBED_DIR / EMBED_FILE_NAME

    def _get_fastest_embed_url(self) -> str:
        json_config = config.get_json_config()

        if fastest_url := json_config.get("url.embed", ""):
            return fastest_url
        else:
            fastest_url = get_fastest_url(config.EMBED_URL_PREFIX)
            json_config["url.embed"] = fastest_url
            return fastest_url

    def pack(self):
        runtime_dir = self.dest_dir / "runtime"
        embed_file_path = self.EMBED_FILEPATH

        if (runtime_dir / "python.exe").exists():
            logging.warning("目标文件夹 [purple]runtime[/] 已存在, 跳过 [bold green]:heavy_check_mark:")
            return

        if embed_file_path.exists():
            logging.info("找到本地 [green bold]embed 压缩包")
            logging.info(f"检查校验和: [green underline]{embed_file_path.name} [bold green]:heavy_check_mark:")
            src_checksum = config.get_json_config().get("file.embed.checksum", "")
            dst_checksum = calc_checksum(embed_file_path)

            if src_checksum == dst_checksum:
                logging.info("校验和一致, 使用[bold green] 本地运行时 :heavy_check_mark:")
            else:
                logging.info("校验和不一致, 重新下载")
                self._fetch_runtime()
        else:
            if not self.mode.offline:
                logging.info("非离线模式, 获取运行时")
                self._fetch_runtime()
            else:
                logging.error(f"离线模式且本地运行时不存在: [bold red]{embed_file_path}[/], 退出")
                return

        logging.info(
            f"解压 runtime 文件: [green underline]{self.EMBED_FILEPATH.name} "
            f"-> {runtime_dir.relative_to(self.root_dir)}[/] [bold green]:heavy_check_mark:"
        )
        shutil.unpack_archive(self.EMBED_FILEPATH, runtime_dir, "zip")

    def _fetch_runtime(self):
        fastest_url = self._get_fastest_embed_url()
        archive_url = f"{fastest_url}{config.PYTHON_VER}/{self.EMBED_FILE_NAME}"
        json_config = config.get_json_config()

        if not archive_url.startswith("https://"):
            logging.error(f"无效 url 路径: {archive_url}")
            typer.Exit(code=2)

        content = safe_read_url_data(archive_url)
        if content is None:
            logging.error("下载运行时失败")
            typer.Exit(code=2)

        logging.info(f"从地址下载运行时: [[green bold]{fastest_url}[/]]")
        t0 = time.perf_counter()

        if not self.EMBED_DIR.exists():
            self.EMBED_DIR.mkdir(exist_ok=True, parents=True)

        with open(self.EMBED_FILEPATH, "wb") as f:
            f.write(content)

        download_time = time.perf_counter() - t0
        logging.info(f"下载完成, 用时: [green bold]{download_time:.2f}s")

        checksum = calc_checksum(self.EMBED_FILEPATH)
        logging.info(f"更新校验和 [{checksum}]")
        json_config["file.embed.checksum"] = checksum
