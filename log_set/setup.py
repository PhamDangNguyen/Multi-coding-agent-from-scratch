import logging
import json
from typing import Optional, Any

from rich.logging import RichHandler


class AppLogger:
    _initialized = False

    @classmethod
    def _setup(cls):
        if cls._initialized:
            return

        handler = RichHandler(
            rich_tracebacks=True,
            markup=True,
            show_time=True,
            show_level=True,
            show_path=False,
        )

        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(handler)

        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)

        cls._initialized = True

    def __init__(self, name: Optional[str] = None):
        self._setup()
        self.logger = logging.getLogger(name if name else __name__)

    def _format(self, message: Any) -> str:
        if isinstance(message, (dict, list)):
            return json.dumps(message, indent=2, ensure_ascii=False)

        if isinstance(message, str):
            try:
                parsed = json.loads(message)
                return json.dumps(parsed, indent=2, ensure_ascii=False)
            except Exception:
                return message

        return str(message)

    # ========================
    # Core logging
    # ========================
    def log(self, level: str, message: Any, **kwargs):
        message = self._format(message)

        if kwargs:
            extra = " ".join(f"{k}={v}" for k, v in kwargs.items())
            message = f"{message}\n{extra}"

        level = level.upper()

        if level == "DEBUG":
            self.logger.debug(message)
        elif level == "INFO":
            self.logger.info(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "ERROR":
            self.logger.error(message)
        elif level == "CRITICAL":
            self.logger.critical(message)
        else:
            self.logger.info(message)

    def info(self, msg: Any, **kwargs):
        self.log("INFO", msg, **kwargs)

    def debug(self, msg: Any, **kwargs):
        self.log("DEBUG", msg, **kwargs)

    def warning(self, msg: Any, **kwargs):
        self.log("WARNING", msg, **kwargs)

    def error(self, msg: Any, **kwargs):
        self.log("ERROR", msg, **kwargs)

    def critical(self, msg: Any, **kwargs):
        self.log("CRITICAL", msg, **kwargs)