from httpx import AsyncClient
from core.api import app 
from config.config import Config
from config import logging_config
logging = logging_config.setup_logging(__name__)

# Тестовые данные
API_KEY = "adminapi007" 
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
TEST_MESSAGE = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": f"{Config.test_request}"}],
    "temperature": 0.7
}
EXPECTED_RESPONSE = Config.test_response

async def test_chat_completions():
    async with app.router.lifespan_context(app) as lifespan:
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            try:
                response = await client.post("/v1/chat/completions", json=TEST_MESSAGE, headers=HEADERS)
                assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
                assert response.json()["response"] == EXPECTED_RESPONSE, f"Expected response '{EXPECTED_RESPONSE}', but got '{response.json()['response']}'"
            except:
                logging.error("The bot's response does not contain the word 'Тест'")
            finally:
                logging.info("Test passed!")


