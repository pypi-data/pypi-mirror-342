import logging
import os
from datetime import datetime
from pathlib import Path
from ..config.app_config import APP_ENV

# Get project root directory


def get_project_root():
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if parent.name == 'cli':
            return parent
    return current_path.parents[2]  # Fallback to 2 levels up from logger.py


ROOT_DIR = get_project_root()

# Set date format
date = datetime.now()
date_str = f"{date.year}-{date.month}-{date.day}"


def create_dir_if_not_exist(dir_name: str):
    """Create directory if it doesn't exist"""
    dir_path = os.path.join(ROOT_DIR, dir_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


# Define log formatter
class CustomFormatter(logging.Formatter):
    def __init__(self, worker_id: str = 'main'):
        super().__init__(fmt='[%(levelname)s] - [%(asctime)s] [%(worker_id)s] %(message)s',
                         datefmt='%Y-%m-%d %H:%M:%S.%f')
        self.worker_id = worker_id

    def format(self, record):
        record.worker_id = self.worker_id
        return super().format(record)


# Create logs directory
create_dir_if_not_exist('logs')
create_dir_if_not_exist('logs/cli')

# Create CLI Logger
cli_logger = logging.getLogger('cli_logger')
cli_logger.setLevel(logging.DEBUG)

# Prevent duplicate logs if logger is imported multiple times
if not cli_logger.handlers:
    # File handler
    cli_log_file = os.path.join(ROOT_DIR, f'logs/cli/{date_str}.log')
    fh_cli = logging.FileHandler(cli_log_file, encoding='utf-8')
    fh_cli.setLevel(logging.DEBUG)
    fh_cli.setFormatter(CustomFormatter())
    cli_logger.addHandler(fh_cli)

    # Console handler: 仅在开发环境或DEBUG_STDIO_RUNNER=1时输出到终端
    # if APP_ENV == "dev":
    ch_cli = logging.StreamHandler()
    ch_cli.setLevel(logging.DEBUG)
    ch_cli.setFormatter(CustomFormatter())
    cli_logger.addHandler(ch_cli)


def verbose(message: str) -> None:
    """Logs a verbose message to both file and console (if INFO level)"""
    cli_logger.debug(message)


# For compatibility with existing code
debug = cli_logger.debug
info = cli_logger.info
warning = cli_logger.warning
error = cli_logger.error
critical = cli_logger.critical
