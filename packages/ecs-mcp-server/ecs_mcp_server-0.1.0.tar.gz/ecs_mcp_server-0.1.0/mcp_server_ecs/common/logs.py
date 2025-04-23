import functools
import json
import logging
import os
from concurrent_log_handler import ConcurrentRotatingFileHandler
from typing import Any, Callable, TypeVar, cast
from mcp_server_ecs.conf.config import log_config

_WRITE_MODE = "a"
T = TypeVar("T")

LOG = logging.getLogger(__name__)
LOG.propagate = False

try:
    LOG.setLevel(getattr(logging, log_config.level.upper(), logging.INFO))
    log_dir = os.path.dirname(log_config.file)
    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s %(filename)s line:%(lineno)d %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    rotate_handler = ConcurrentRotatingFileHandler(
        log_config.file,
        _WRITE_MODE,
        log_config.max_size,
        log_config.backup_count,
    )
    rotate_handler.setLevel(logging.INFO)
    rotate_handler.setFormatter(formatter)
    LOG.addHandler(rotate_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    LOG.addHandler(console_handler)

except Exception as e:
    print(f"Log initialize failed: {str(e)}")


def log_params(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator, used to record function parameters in logs
    """

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            params = args[1] if len(args) > 1 else kwargs.get("params")
            if params is not None:
                params_dict = {k: v for k, v in vars(
                    params).items() if v is not None}
                LOG.info(
                    "Tool: %s, Params:\n%s",
                    func.__name__,
                    json.dumps(params_dict, indent=2, ensure_ascii=False),
                )
            return await func(*args, **kwargs)
        except Exception as e:
            LOG.error("Error in log_params decorator: %s", str(e))
            return await func(*args, **kwargs)

    return cast(Callable[..., T], wrapper)
