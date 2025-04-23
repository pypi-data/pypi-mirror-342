import json
import logging
import os
import sys
import traceback
from datetime import datetime
from types import TracebackType
from typing import Optional, Type


class LocalExceptionLogger:
    def __init__(self, report_dir: str = "crash_reports", max_breadcrumbs: int = 100):
        self.report_dir = report_dir
        self.max_breadcrumbs = max_breadcrumbs
        self.breadcrumbs = []

        os.makedirs(self.report_dir, exist_ok=True)
        self._setup_logging()
        sys.excepthook = self._handle_exception

    def _setup_logging(self):
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Console output
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        root_logger.addHandler(ch)

        bh = self.BreadcrumbHandler(self)
        bh.setLevel(logging.DEBUG)
        bh.setFormatter(formatter)
        root_logger.addHandler(bh)

    class BreadcrumbHandler(logging.Handler):
        def __init__(self, exception_logger):
            super().__init__()
            self.exception_logger = exception_logger

        def emit(self, record):
            if (
                len(self.exception_logger.breadcrumbs)
                >= self.exception_logger.max_breadcrumbs
            ):
                self.exception_logger.breadcrumbs.pop(0)
            self.exception_logger.breadcrumbs.append(self.format(record))

    def _extract_stack_info(self, tb: Optional[TracebackType]):
        frames = []
        while tb:
            frame = tb.tb_frame
            frames.append(
                {
                    "file": frame.f_code.co_filename,
                    "line": tb.tb_lineno,
                    "function": frame.f_code.co_name,
                    "locals": {k: repr(v) for k, v in frame.f_locals.items()},
                }
            )
            tb = tb.tb_next
        return frames

    def _handle_exception(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType,
    ):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(self.report_dir, f"crash_{timestamp}.json")

        crash_data = {
            "timestamp": timestamp,
            "exception_type": str(exc_type),
            "message": str(exc_value),
            "traceback": traceback.format_exception(exc_type, exc_value, exc_traceback),
            "stack_frames": self._extract_stack_info(exc_traceback),
            "breadcrumbs": self.breadcrumbs,
        }

        with open(report_file, "w") as f:
            json.dump(crash_data, f, indent=2)

        print(f"\n⚠️ Crash report saved: {report_file}")
