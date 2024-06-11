import logging

# Определяем ANSI escape-коды для цветов
RESET = "\x1b[0m"
WHITE = "\x1b[0m"
COLORS = {
    'DEBUG': "\x1b[34m",      # Синий
    'INFO': "\x1b[32m",       # Зеленый
    'WARNING': "\x1b[33m",    # Желтый
    'ERROR': "\x1b[31m",      # Красный
    'CRITICAL': "\x1b[41m",   # Красный фон
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_color = COLORS.get(record.levelname, RESET)
        message = super().format(record)
        return f"{log_color}{record.levelname}{RESET}{WHITE}: {message}{RESET}"

def setup_logging(name='my_app', level=logging.DEBUG, enable_detailed_logs=True):
    logger = logging.getLogger(name)
    if not logger.handlers:  # Проверяем, есть ли уже обработчики у логгера
        handler = logging.StreamHandler()
        formatter = ColoredFormatter('    %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        if enable_detailed_logs:
            logger.setLevel(level)
        else:
            logger.setLevel(logging.INFO) # Уровень лога
    return logger


