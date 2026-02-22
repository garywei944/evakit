import logging
from typing import Any

__all__ = ["setup_root_logger", "log_header"]

logger = logging.getLogger(__name__)


def setup_root_logger(
    process_info: bool = True, full_path: bool = True, clear_root_handlers: bool = True
):
    """Setup the root logger with a specific format.

    By default, the root logger format will be propagated to all child loggers, so we
    don't need to setup loggers for each module.
    """

    if clear_root_handlers:
        logging.root.handlers.clear()

    segs = ["%(levelname).1s%(asctime)s.%(msecs)03d"]

    if process_info:
        segs.append("[%(process)d:%(processName)s]")

    segs.append("[%(thread)x:%(threadName)s]")

    loc = "%(pathname)s:%(lineno)d" if full_path else "%(name)s:%(lineno)d"
    segs.append(f"{loc}::%(funcName)s - %(message)s")

    logging.basicConfig(
        level=logging.DEBUG,
        format=" ".join(segs),
        datefmt="%m%d %H:%M:%S",
        force=True,
    )


def log_header(header: str, content: Any, header_length: int = 40, log_level: int = logging.DEBUG):
    """Log the content with a header, the header will be centered and padded with '='."""
    logger.log(
        log_level,
        "%s %s %s\n\n%s\n",
        "=" * 20,
        header.center(header_length - 2),
        "=" * 30,
        content,
    )
