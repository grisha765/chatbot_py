from httpx import AsyncClient
from core.api import app 
from config.config import Config
from config import logging_config
logging = logging_config.setup_logging(__name__)

# Тестовые данные
API_KEY = "adminapi007" 
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
TEST_MESSAGES = [
    {
        "model": "gpt-3.5-duck",
        "messages": [{"role": "user", "content": f"{Config.test_request}"}],
        "temperature": 0.7
    },
    {
        "model": "llama3-duck",
        "messages": [{"role": "user", "content": f"{Config.test_request}"}],
        "temperature": 0.7
    }
]
EXPECTED_RESPONSE = Config.test_response

async def test_chat_completions():
    async with app.router.lifespan_context(app):
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            for test_message in TEST_MESSAGES:
                model = test_message["model"]
                try:
                    response = await client.post("/v1/chat/completions", json=test_message, headers=HEADERS)
                    assert response.status_code == 200, f"{model}: Expected status code 200, but got {response.status_code}"
                    assert response.json()["choices"][0]["message"]["content"] == EXPECTED_RESPONSE, f"{model}: Expected response '{EXPECTED_RESPONSE}', but got '{response.json()['choices'][0]['message']['content']}'"

                    logging.info(f'{"\x1b[32m"}{model}: Test passed!{"\x1b[0m"}')
                except Exception as e:
                    logging.warning(f"{model}: The bot's response does not contain the expected response", e)

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
