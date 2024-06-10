import asyncio
import signal
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
from contextlib import asynccontextmanager

from chat_bot import init_browser, prepare_page, send_message_fastapi

import logging_config
logging = logging_config.setup_logging(name='api', enable_detailed_logs=True)

app = FastAPI()

# Глобальные переменные для браузера и страницы
browser = None
page = None

# Список API ключей
API_KEYS = {
    "adminapi007": "admin",
    # Добавьте другие API ключи здесь
}

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: float

async def process_message(messages: List[Message]) -> str:
    global page
    # Отправляем сообщения по порядку и получаем ответ
    response = ""
    for message in messages:
        logging.info(f"Sending message: {message.content}")
        response = await send_message_fastapi(page, message.content)
        logging.info(f"Received response: {response}")
    return response

@asynccontextmanager
async def lifespan(app: FastAPI):
    global browser, page
    logging.info("Initializing browser and page")
    browser, page = await init_browser()
    await prepare_page(page)
    try:
        yield
    finally:
        logging.info("Closing browser")
        await browser.close()

app.router.lifespan_context = lifespan

@app.post("/v1/chat/completions")
async def chat_completions(request: Request, chat_request: ChatRequest):
    # Проверка API ключа
    api_key = request.headers.get("Authorization")
    if not api_key or api_key.split(" ")[1] not in API_KEYS:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        response = await process_message(chat_request.messages)
        return {"response": response}
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def handle_exit(sig, frame):
    logging.info("Shutting down server...")
    asyncio.get_event_loop().stop()

def run_server():
    import uvicorn
    config = uvicorn.Config("api:app", host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(config)

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, handle_exit, signal.SIGINT, None)
    loop.add_signal_handler(signal.SIGTERM, handle_exit, signal.SIGTERM, None)
    
    asyncio.ensure_future(server.serve())
    loop.run_forever()

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")

