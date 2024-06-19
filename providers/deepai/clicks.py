import asyncio
from config import logging_config

logging = logging_config.setup_logging(__name__)

async def clickss(page, message):
    try:
        # Ввод текста в поле ввода
        logging.debug(f"Typing text: {message}")
        textareas = await page.query_selector_all('textarea[placeholder*="Chat with AI..."]')
        empty_textarea = None
        for textarea in textareas:
            value = await textarea.evaluate('(element) => element.value')
            if value == "":
                empty_textarea = textarea
                break
        if empty_textarea:
            try:
                # Ввод текста в пустое поле ввода
                await empty_textarea.fill(message)
            except Exception as e:
                logging.error(f"Error typing text '{message}': {e}")
                return
        else:
            logging.error("No empty textarea found.")
            return
    except Exception as e:
        logging.error(f"Error typing text '{message}': {e}")
        return

    await asyncio.sleep(1)

    try:
        # Нажимаем кнопку отправки
        logging.debug("Clicking 'Send' button...")
        send_button = await page.query_selector("#chatSubmitButton")
        await send_button.click()
    except Exception as e:
        logging.error(f"Error clicking 'Send' button: {e}")

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
