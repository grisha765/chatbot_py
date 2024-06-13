import asyncio
from config import logging_config

logging = logging_config.setup_logging(__name__)

def process_string(text, convert_to_lower):
    if convert_to_lower:
        return text.lower()
    else:
        return text

async def clickss(page, message, provider, convert_to_lower):
    try:
        textarea = await page.query_selector('textarea')
        text_content = await textarea.get_attribute('placeholder')
    except Exception as e:
        logging.error(f"Error querying textarea or evaluating placeholder: {e}")
        return

    if provider not in text_content:
        try:
            logging.debug("Clicking 'Change provider' button...")
            buttons = await page.query_selector_all('[data-reach-tooltip-trigger]')
            await buttons[0].click()
        except Exception as e:
            logging.error(f"Error clicking 'Change provider' button: {e}")
            return

        try:
            logging.debug(f"Clicking 'Change to {provider}' button...")
            await page.wait_for_selector(f'label[for*="{process_string(provider, convert_to_lower)}"]')
            label = await page.query_selector(f'label[for*="{process_string(provider, convert_to_lower)}"]')
            await label.click()
        except Exception as e:
            logging.error(f"Error clicking 'Change to {provider}' button: {e}")
            return

        try:
            logging.debug("Clicking 'Start New Chat' button...")
            buttons = await page.query_selector_all('button')
            for button in buttons:
                text = await button.text_content()
                if 'Start New Chat' in text:
                    await button.click()
                    break
        except Exception as e:
            logging.error(f"Error clicking 'Start New Chat' button: {e}")
            return

    try:
        # Ввод текста в поле ввода
        logging.debug(f"Typing text: {message}")
        await page.fill(f'textarea[placeholder*="Chat with {provider}"]', message)
    except Exception as e:
        logging.error(f"Error typing text '{message}': {e}")
        return

    await asyncio.sleep(1)

    try:
        # Нажимаем кнопку отправки
        logging.debug("Clicking 'Send' button...")
        send_button = await page.query_selector('button[aria-label="Send"]')
        await send_button.click()
    except Exception as e:
        logging.error(f"Error clicking 'Send' button: {e}")

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")

