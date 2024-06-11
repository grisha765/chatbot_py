import asyncio

from providers.ddgo.clicks import clickss
from config import logging_config
logging = logging_config.setup_logging(__name__)

# Функция для отправки сообщения и получения ответа
async def send_message(page, message, screenshot_path=None):
    await clickss(page, message, "Llama", False)
    # Динамическое ожидание появления нового ответа
    logging.debug("Waiting for response...")
    last_response = ""
    while True:
        await asyncio.sleep(1)
        response_elements = await page.querySelectorAll('div > div:nth-child(2) > div:nth-child(2)')
        if response_elements:
            current_response = await page.evaluate('(element) => element.innerText', response_elements[-1])
            if current_response != last_response:
                last_response = current_response
            else:
                break
    
    # Делаем скриншот, если указан путь
    if screenshot_path:
        logging.info(f"Saving screenshot to {screenshot_path}")
        await page.screenshot({'path': screenshot_path})

    return last_response

# Функция для FastAPI, возвращающая ответ без печати
async def send_message_fastapi(page, message):
    await clickss(page, message, "Llama", False)
    # Динамическое ожидание появления нового ответа
    logging.info("Waiting for response...")
    last_response = ""
    while True:
        await asyncio.sleep(1)
        response_elements = await page.querySelectorAll('div > div:nth-child(2) > div:nth-child(2)')
        if response_elements:
            current_response = await page.evaluate('(element) => element.innerText', response_elements[-1])
            if "Generating response..." in current_response:
                continue
            if current_response != last_response:
                last_response = current_response
            else:
                break

    # Нажимаем кнопку очистки
    await asyncio.sleep(1)
    buttons = await page.querySelectorAll('[data-reach-tooltip-trigger]')
    if len(buttons) >= 4:
        await buttons[3].click()
        logging.debug("Clicking 'Clear' button...")
    else:
        logging.error("The required button was not found.")

    # Возвращаем ответ
    return last_response

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
