class Config():
    api_host: str = '127.0.0.1'
    api_port: int = 8000
    log_level: str = "DEBUG"
    api_keys = {
        "adminapi007": "admin",
        "userapi008": "user"
        # Добавьте другие API ключи здесь
    }
    test_request: str = "Напиши мне слово Тест и ничего более!"
    test_response: str = "Тест"
