"""Logging system for PDF to Markdown converter."""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class Logger:
    """Custom logger with daily log rotation and detailed context."""

    _loggers: dict = {}

    def __new__(cls, name: str, logs_dir: str = "logs"):
        """Get or create logger instance for given name."""
        key = f"{name}:{logs_dir}"
        if key not in cls._loggers:
            instance = super().__new__(cls)
            instance._name = name
            instance._logs_dir = logs_dir
            instance._logger = cls._setup_logger(name, logs_dir)
            cls._loggers[key] = instance
        return cls._loggers[key]

    @staticmethod
    def _setup_logger(name: str, logs_dir: str) -> logging.Logger:
        """Setup logger with daily log file and console handler."""
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Remove existing handlers to avoid duplicates
        logger.handlers.clear()

        # Ensure logs directory exists
        os.makedirs(logs_dir, exist_ok=True)

        # Daily log file
        log_filename = f"{datetime.now().strftime('%Y-%m-%d')}.log"
        log_filepath = os.path.join(logs_dir, log_filename)

        # File handler
        file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter with detailed context
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def _get_caller_info(self) -> tuple:
        """Get caller class name and line number."""
        import inspect
        frame = inspect.currentframe()
        if frame is None:
            return "", 0

        # Go up the stack to find the actual caller
        # Skip _get_caller_info and the log method
        frame = frame.f_back.f_back.f_back

        if frame is None:
            return "", 0

        # Try to get class name from frame
        frame_locals = frame.f_locals
        class_name = ""
        if 'self' in frame_locals:
            class_name = frame_locals['self'].__class__.__name__
        elif 'cls' in frame_locals:
            class_name = frame_locals['cls'].__name__

        line_no = frame.f_lineno
        return class_name, line_no

    def debug(self, message: str, **kwargs):
        """Log debug message."""
        class_name, line_no = self._get_caller_info()
        extra_info = ""
        if kwargs:
            extra_info = f" | Params: {kwargs}"
        self._logger.debug(f"[{class_name}:{line_no}] {message}{extra_info}")

    def info(self, message: str, **kwargs):
        """Log info message."""
        class_name, line_no = self._get_caller_info()
        extra_info = ""
        if kwargs:
            extra_info = f" | Params: {kwargs}"
        self._logger.info(f"[{class_name}:{line_no}] {message}{extra_info}")

    def warning(self, message: str, **kwargs):
        """Log warning message."""
        class_name, line_no = self._get_caller_info()
        extra_info = ""
        if kwargs:
            extra_info = f" | Params: {kwargs}"
        self._logger.warning(f"[{class_name}:{line_no}] {message}{extra_info}")

    def error(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log error message with exception details."""
        class_name, line_no = self._get_caller_info()
        extra_info = ""
        if kwargs:
            extra_info = f" | Params: {kwargs}"
        if exception:
            extra_info += f" | Exception: {type(exception).__name__}: {str(exception)}"
        self._logger.error(f"[{class_name}:{line_no}] {message}{extra_info}")

    def critical(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log critical message with exception details."""
        class_name, line_no = self._get_caller_info()
        extra_info = ""
        if kwargs:
            extra_info = f" | Params: {kwargs}"
        if exception:
            extra_info += f" | Exception: {type(exception).__name__}: {str(exception)}"
        self._logger.critical(f"[{class_name}:{line_no}] {message}{extra_info}")

    def log_page_progress(self, current_page: int, total_pages: int, action: str = "Processing"):
        """Log PDF page processing progress.

        Args:
            current_page: Current page number (1-indexed)
            total_pages: Total number of pages
            action: Action being performed (default: "Processing")
        """
        self.info(f"{action} PDF page {current_page}/{total_pages}",
                  current_page=current_page,
                  total_pages=total_pages)

    def log_progress(self, completed: int, total: int, failed: int = 0,
                     average_time: float = 0, estimated_remaining: float = 0):
        """Log conversion progress with time estimation.

        Args:
            completed: Number of completed pages
            total: Total number of pages
            failed: Number of failed pages
            average_time: Average processing time per page (seconds)
            estimated_remaining: Estimated remaining time (seconds)
        """
        progress_percent = round((completed / total * 100) if total > 0 else 0, 2)
        self.info(
            f"Progress: {progress_percent}% ({completed}/{total} completed, {failed} failed)",
            completed=completed,
            total=total,
            failed=failed,
            average_time=average_time,
            estimated_remaining=estimated_remaining
        )

    def log_time_estimation(self, current_page: int, total_pages: int,
                           average_time: float, total_elapsed: float):
        """Log time estimation.

        Args:
            current_page: Current page being processed
            total_pages: Total number of pages
            average_time: Average time per page (seconds)
            total_elapsed: Total elapsed time so far (seconds)
        """
        remaining = total_pages - current_page
        estimated = remaining * average_time if average_time > 0 else 0

        self.info(
            f"Time estimation: Page {current_page}/{total_pages}",
            current_page=current_page,
            total_pages=total_pages,
            average_time=average_time,
            total_elapsed=total_elapsed,
            estimated_remaining=estimated
        )

    def print_progress(self, completed: int, total: int, failed: int = 0,
                      average_time: float = 0, estimated_remaining: float = 0,
                      current_page: Optional[int] = None):
        """Print progress to console (bypasses logging).

        Args:
            completed: Number of completed pages
            total: Total number of pages
            failed: Number of failed pages
            average_time: Average processing time per page (seconds)
            estimated_remaining: Estimated remaining time (seconds)
            current_page: Current page being processed (optional)
        """
        progress_percent = round((completed / total * 100) if total > 0 else 0, 2)

        status = "Processing" if completed < total else "Completed"
        if current_page:
            status += f" page {current_page}/{total}"

        print(f"\r[{status}] Progress: {progress_percent}% "
              f"({completed}/{total} done, {failed} failed)", end='', flush=True)

        if completed == total or estimated_remaining > 0:
            print()  # New line after completion or when we have time estimate
            if average_time > 0:
                remaining_str = self._format_time(estimated_remaining)
                print(f"  Average: {self._format_time(average_time)}/page | "
                      f"Estimated remaining: {remaining_str}")

    @staticmethod
    def _format_time(seconds: float) -> str:
        """Format time duration.

        Args:
            seconds: Duration in seconds

        Returns:
            Formatted time string
        """
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            return f"{hours}h {minutes}m {secs}s"


def get_logger(name: str, logs_dir: str = "logs") -> Logger:
    """Get logger instance for given name.

    Args:
        name: Logger name (typically class name or module name)
        logs_dir: Directory for log files

    Returns:
        Logger instance
    """
    return Logger(name, logs_dir)