import os
class Config():
    api_host: str = os.getenv('API_HOST', '127.0.0.1')
    api_port: int = int(os.getenv('API_PORT', 8000))
    log_level: str = os.getenv('LOG_LEVEL', "DEBUG")
    api_keys = {
        "adminapi007": "admin",
        "userapi008": "user"
        # Добавьте другие API ключи здесь
    }
    test_request: str = os.getenv('TEST_REQUEST', "Write me the word Test and nothing more!")
    test_response: str = os.getenv('TEST_RESPONSE', "Test")
