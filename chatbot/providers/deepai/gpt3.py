import asyncio
from chatbot.providers.deepai.clicks import clickss
from chatbot.config import logging_config

logging = logging_config.setup_logging(__name__)

# Функция для отправки сообщения и получения ответа
async def send_message(page, message, screenshot_path=None, temp=False):
    await clickss(page, message)
    # Динамическое ожидание появления нового ответа
    logging.debug("Waiting for response...")
    # Получаем текущее количество outputBox элементов
    initial_count = len(await page.query_selector_all("div.outputBox"))

    try:
        while True:
            # Ожидание появления нового ответа
            await asyncio.sleep(1)  # Задержка для предотвращения слишком частых проверок
            current_count = len(await page.query_selector_all("div.outputBox p"))
            if current_count > initial_count:
                # Появился новый элемент outputBox
                output_boxes = await page.query_selector_all("div.outputBox p")
                if output_boxes:
                    last_output_box = output_boxes[-1]
                    last_response = await last_output_box.inner_text()
                    return last_response
                else:
                    logging.error("Output boxes not found.")
                break
    except TimeoutError:
        logging.error("The .outputBox element was not found within the specified time.")
    
    # Делаем скриншот, если указан путь
    if screenshot_path:
        logging.info(f"Saving screenshot to {screenshot_path}")
        await page.screenshot(path=screenshot_path)

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
