import logging

from rich.logging import RichHandler

from fspacker import config


def setup_logging(debug_mode: bool = False):
    """配置日志"""

    config.get_json_config()["mode.debug"] = debug_mode

    if debug_mode:
        logging.basicConfig(
            level=logging.DEBUG, format="[*] %(message)s", datefmt="[%X]", handlers=[RichHandler(markup=True)]
        )
    else:
        logging.basicConfig(
            level=logging.INFO, format="[*] %(message)s", datefmt="[%X]", handlers=[RichHandler(markup=True)]
        )
