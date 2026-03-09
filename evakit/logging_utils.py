import atexit
import logging
import logging.handlers
import queue
from typing import Any

__all__ = ["setup_root_logger", "log_header"]

logger = logging.getLogger(__name__)

_queue = queue.Queue[Any]()
_listener: logging.handlers.QueueListener | None = None
_atexit_registered = False


def _shutdown_logging():
    global _listener
    if _listener is not None:
        _listener.stop()


def setup_root_logger(process_info: bool = True, full_path: bool = True, clear_root_handlers: bool = True):
    global _queue, _listener, _atexit_registered

    if not _atexit_registered:
        atexit.register(_shutdown_logging)
        _atexit_registered = True

    root = logging.getLogger()

    # Stop previous listener if it exists. This flush the pending log records.
    if _listener is not None:
        _listener.stop()
        _listener = None
        _queue = queue.Queue[Any]()

    if clear_root_handlers:
        root.handlers.clear()

    segs = ["%(levelname).1s%(asctime)s.%(msecs)03d"]

    if process_info:
        segs.append("[%(process)d:%(processName)s]")

    segs.append("[%(thread)x:%(threadName)s]")

    loc = "%(pathname)s:%(lineno)d" if full_path else "%(name)s:%(lineno)d"
    segs.append(f"{loc}::%(funcName)s - %(message)s")

    formatter = logging.Formatter(
        " ".join(segs),
        datefmt="%m%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    queue_handler = logging.handlers.QueueHandler(_queue)
    _listener = logging.handlers.QueueListener(
        _queue,
        stream_handler,
        respect_handler_level=True,
    )

    root.setLevel(logging.DEBUG)
    root.addHandler(queue_handler)

    _listener.start()


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
