import asyncio
from config import logging_config
logging = logging_config.setup_logging(__name__)

def process_string(text, convert_to_lower):
    if convert_to_lower:
        return text.lower()
    else:
        return text

async def clickss(page, message, provider, convert_to_lower):
    textarea = await page.querySelector('textarea')
    text_content = await page.evaluate('(textarea) => textarea.placeholder', textarea)
    if provider not in text_content:
        logging.debug("Clicking 'Change provider' button...")
        buttons = await page.querySelectorAll('[data-reach-tooltip-trigger]')
        await buttons[0].click()
        logging.debug(f"Clicking 'Change to {provider}' button...")
        await page.waitForSelector(f'label[for*="{process_string(provider, convert_to_lower)}"]')
        label = await page.querySelector(f'label[for*="{process_string(provider, convert_to_lower)}"]')
        await label.click()
        logging.debug("Clicking 'Start New Chat' button...")
        buttons = await page.querySelectorAll('button')
        for button in buttons:
            text = await page.evaluate('(button) => button.textContent', button)
            if 'Start New Chat' in text:
                await button.click()
                break

    # Ввод текста в поле ввода
    logging.debug(f"Typing text: {message}")
    await page.type(f'textarea[placeholder*="Chat with {provider}"]', message)

    await asyncio.sleep(1)
    
    # Нажимаем кнопку отправки
    logging.debug("Clicking 'Send' button...")
    send_button = await page.querySelector('button[aria-label="Send"]')
    await send_button.click()
