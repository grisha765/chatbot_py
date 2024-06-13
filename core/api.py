import asyncio
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
from contextlib import asynccontextmanager

from core.browser import init_browser
from providers.ddgo.start import prepare_page
from providers.ddgo.gpt3 import send_message_fastapi as send_message_gpt3
from providers.ddgo.llama3 import send_message_fastapi as send_message_llama3
from config import logging_config
from config.config import Config
logging = logging_config.setup_logging(__name__)

app = FastAPI()

# Глобальные переменные для браузера и страницы
browser = None
page = None

# Список API ключей
API_KEYS = Config.api_keys 

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: float

async def process_message(model:str, messages: List[Message]) -> str:
    global page
    # Отправляем сообщения по порядку и получаем ответ
    response = ""
    if model == "gpt-3.5-duck":
        for message in messages:
            logging.info(f"Sending message to {model}: {message.content}")
            response = await send_message_gpt3(page, message.content)
            logging.info(f"Received response from {model}: {response}")
    elif model == "llama3-duck":
        for message in messages:
            logging.info(f"Sending message to {model}: {message.content}")
            response = await send_message_llama3(page, message.content)
            logging.info(f"Received response from {model}: {response}")
    else:
        raise HTTPException(status_code=400, detail="Invalid model specified")
    return response

@asynccontextmanager
async def lifespan(app: FastAPI):
    global browser, page
    logging.info("Initializing browser and page")
    browser, page, playwright = await init_browser()
    await prepare_page(page)
    try:
        yield
    finally:
        logging.info("Closing browser")
        if browser:
            try:
                await browser.close()
            except Exception as e:
                logging.error(f"An error occurred while closing the browser: {e}")
        if playwright:
            try:
                await playwright.stop()
            except Exception as e:
                logging.error(f"An error occurred while stopping playwright: {e}")

app.router.lifespan_context = lifespan

@app.post("/v1/chat/completions")
async def chat_completions(request: Request, chat_request: ChatRequest):
    # Проверка API ключа
    api_key = request.headers.get("Authorization")
    if not api_key or api_key.split(" ")[1] not in API_KEYS:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        response = await process_message(chat_request.model, chat_request.messages)
        return {
            "id": "chatcmpl-12345",
            "object": "chat.completion",
            "created": 1677631234,
            "model": chat_request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response
                    },
                    "finish_reason": "stop"
                }
            ]
        }
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def run_server():
    import uvicorn
    uvicorn.run("core.api:app", host=Config.api_host, port=Config.api_port, log_level="info")

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")

