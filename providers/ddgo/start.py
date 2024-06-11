import asyncio

from config import logging_config
logging = logging_config.setup_logging(__name__)

# Функция для навигации и подготовки страницы
async def prepare_page(page):
    logging.info("Navigating to DuckDuckGo AI Chat...")
    await page.goto('https://duckduckgo.com/?q=DuckDuckGo&ia=chat')
    
    # Ждем, пока страница полностью загрузится
    await page.waitForSelector('button')
    
    # Нажимаем на кнопку с текстом "Get Started"
    logging.debug("Clicking 'Get Started' button...")
    buttons = await page.querySelectorAll('button')
    for button in buttons:
        text = await page.evaluate('(button) => button.textContent', button)
        if 'Get Started' in text:
            await button.click()
            break
    
    # Ждем появления кнопки "Next"
    await page.waitForSelector('button')

    # Нажимаем на кнопку с текстом "Next"
    logging.debug("Clicking 'Next' button...")
    buttons = await page.querySelectorAll('button')
    for button in buttons:
        text = await page.evaluate('(button) => button.textContent', button)
        if 'Next' in text:
            await button.click()
            break

    # Ждем появления кнопки "I Agree"
    await page.waitForSelector('button')

    # Нажимаем на кнопку с текстом "I Agree"
    logging.debug("Clicking 'I Agree' button...")
    buttons = await page.querySelectorAll('button')
    for button in buttons:
        text = await page.evaluate('(button) => button.textContent', button)
        if 'I Agree' in text:
            await button.click()
            break

    await asyncio.sleep(3)  # ждем 3 секунды
if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
