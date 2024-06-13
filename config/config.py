import os

class Config:
    # Определяем значения по умолчанию
    chrome_path: str = '/bin/chromium'
    api_host: str = '127.0.0.1'
    api_port: int = 8000
    log_level: str = "DEBUG"
    api_keys = {
        "adminapi007": "admin",
        "userapi008": "user"
        # Добавьте другие API ключи здесь
    }
    test_request: str = "Write me the word Test and nothing more!"
    test_response: str = "Test"

    @classmethod
    def load_from_env(cls):
        for key, value in cls.__annotations__.items():
            env_value = os.getenv(key.upper())
            if env_value is not None:
                if isinstance(value, int):
                    setattr(cls, key, int(env_value))
                else:
                    setattr(cls, key, env_value)

# Загружаем конфигурацию из переменных окружения
Config.load_from_env()

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
