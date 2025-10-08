import logging
from src.utils.paths import LOGS_DIR

def get_logger(name: str):
    log_dir = LOGS_DIR
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "pipeline.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # уникаємо дублювання хендлерів при повторному імпорті
    if not logger.handlers:
        handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
