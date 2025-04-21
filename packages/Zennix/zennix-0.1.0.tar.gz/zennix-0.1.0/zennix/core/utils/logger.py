import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # Avoid duplicate handlers

    logger.setLevel(logging.DEBUG)

    # ⏱️ Timestamped filename
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = os.path.join(LOG_DIR, f"zennix-{date_str}.log")

    # 📁 Rotating file handler (~25MB, 25 backups)
    file_handler = RotatingFileHandler(log_filename, maxBytes=5 * 1024 * 1024, backupCount=25)
    file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)

    # ❌ NO console handler
    logger.addHandler(file_handler)

    return logger
