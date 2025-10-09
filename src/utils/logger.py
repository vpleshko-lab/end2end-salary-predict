import logging
from src.utils.paths import LOGS_DIR

def get_logger(name: str):
    """
    Ініціалізація системи логування.

    Створює логер, який одночасно:
      - записує повідомлення у файл (pipeline.log)
      - відображає їх у терміналі

    Аргументи:
        name (str): ім'я логера (наприклад, ім'я модуля)

    Повертає:
        logging.Logger: налаштований логер
    """

    # === Етап 1: Ініціалізація шляху до логів ===
    log_dir = LOGS_DIR
    log_dir.mkdir(exist_ok=True)  # створює директорію, якщо її немає
    log_file = log_dir / "pipeline.log"

    # === Етап 2: Створення логера ===
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # мінімальний рівень повідомлень (INFO і вище)

    # === Етап 3: Перевірка наявності хендлерів ===
    # (щоб уникнути дублювання логів при повторному імпорті)
    if not logger.handlers:

        # --- Хендлер 1: Запис у файл ---
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        file_handler.setFormatter(file_formatter)

        # --- Хендлер 2: Вивід у термінал ---
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            "%(levelname)s | %(message)s"
        )
        console_handler.setFormatter(console_formatter)

        # === Етап 4: Реєстрація хендлерів ===
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
