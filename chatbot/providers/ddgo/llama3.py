import asyncio

from chatbot.providers.ddgo.clicks import clickss
from chatbot.config import logging_config

logging = logging_config.setup_logging(__name__)

# Функция для FastAPI, возвращающая ответ без печати
async def send_message(page, message, screenshot_path=None, temp=False):
    await clickss(page, message, "Llama", False)

    async def wait_for_response(page):
        # Динамическое ожидание появления нового ответа
        logging.info("Waiting for response...")
        last_response = ""
        while True:
            await asyncio.sleep(1)
            response_elements = await page.query_selector_all('div > div:nth-child(2) > div:nth-child(2)')
            if response_elements:
                current_response = await response_elements[-1].inner_text()
                if "Generating response..." in current_response:
                    continue
                if current_response != last_response:
                    last_response = current_response
                else:
                    break
        return last_response

    while True:
        last_response = await wait_for_response(page)
        if "DuckDuckGo AI Chat is temporarily unavailable. Please refresh the page and try again." in last_response:
            logging.warning("DuckDuckGo AI Chat is temporarily unavailable. Refreshing the page...")
            await page.reload()
            await clickss(page, message, "Llama", False)
        else:
            break

    # Нажимаем кнопку очистки если выключен temp
    if temp == False:
        while True:
            await asyncio.sleep(1)
            buttons = await page.query_selector_all('[data-reach-tooltip-trigger]')
            if len(buttons) >= 5:
                await buttons[4].click()
                logging.debug("Clicking 'Clear' button...")
                break
            else:
                logging.error("The required button was not found.")
                await page.reload()
                await clickss(page, message, "Llama", False)
                last_response = await wait_for_response(page)
                if "DuckDuckGo AI Chat is temporarily unavailable. Please refresh the page and try again." not in last_response:
                    continue

    # Делаем скриншот, если указан путь
    if screenshot_path:
        logging.info(f"Saving screenshot to {screenshot_path}")
        await page.screenshot(path=screenshot_path)

    # Возвращаем ответ
    return last_response

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")

