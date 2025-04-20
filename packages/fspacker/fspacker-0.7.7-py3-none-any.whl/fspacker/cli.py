"""应用客户端命令行接口"""

import logging
import os
import pathlib
import subprocess

import typer
from rich.console import Console
from rich.logging import RichHandler

from fspacker import config
from fspacker.exceptions import RunExecutableError
from fspacker.packers.factory import pack
from fspacker.parsers.mode import PackMode
from fspacker.parsers.project import parse_pyproject
from fspacker.trackers import perf_tracker

app = typer.Typer()
console = Console()


def setup_logging(debug_mode: bool = False):
    """配置日志"""

    config.get_json_config()["mode.debug"] = debug_mode
    level = logging.DEBUG if debug_mode else logging.INFO
    logging.basicConfig(level=level, format="[*] %(message)s", datefmt="[%X]", handlers=[RichHandler(markup=True)])


@app.command(name="build", short_help="构建应用程序")
@app.command(name="b", short_help="构建应用程序, 别名: build")
def build(
    archive: bool = typer.Option(False, help="打包模式, 将应用打包为 zip 格式."),
    rebuild: bool = typer.Option(False, help="重构模式, 构建前清理项目文件."),
    debug: bool = typer.Option(False, help="调试模式, 显示调试信息."),
    simplify: bool = typer.Option(False, help="简化模式"),
    use_tk: bool = typer.Option(False, help="打包tk库"),
    offline: bool = typer.Option(False, help="离线模式, 本地构建."),
    directory: str = typer.Argument(None, help="源码目录路径"),
):
    """构建项目命令"""

    mode = PackMode(
        archive=archive,
        rebuild=rebuild,
        debug=debug,
        offline=offline,
        simplify=simplify,
        use_tk=use_tk,
    )
    setup_logging(mode.debug)
    logging.info(mode)

    dirpath = pathlib.Path(directory) if directory is not None else pathlib.Path.cwd()
    pack(root_dir=dirpath, dest_dir=dirpath / "dist", mode=mode)


@app.command(name="version", short_help="显示版本信息")
@app.command(name="v", short_help="显示版本信息, 别名: version")
def version():
    from fspacker import __build_date__
    from fspacker import __version__

    setup_logging()

    console.print(f"fspacker {__version__}, 构建日期: {__build_date__}")


@perf_tracker
def _call_executable(exe_file: pathlib.Path) -> None:
    """调用可执行文件"""

    logging.info(f"调用可执行文件: [green bold]{exe_file}")
    os.chdir(exe_file.parent)
    subprocess.call([str(exe_file)], shell=False)


@app.command(name="run", short_help="运行项目")
@app.command(name="r", short_help="运行项目, 别名: run")
def run(
    directory: str = typer.Argument(None, help="源码目录路径"),
    debug: bool = typer.Option(False, help="调试模式, 显示调试信息."),
):
    """运行项目命令"""

    setup_logging(debug_mode=debug)

    dirpath = pathlib.Path(directory) if directory is not None else pathlib.Path.cwd()
    project_info = parse_pyproject(dirpath)
    exe_files = list(dirpath.rglob(f"{project_info.normalized_name}*.exe"))

    if not len(exe_files):
        raise RunExecutableError("未找到可执行项目文件")

    _call_executable(exe_file=exe_files[0])


def main():
    app()


if __name__ == "__main__":
    main()
