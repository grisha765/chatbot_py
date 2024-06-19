from config import logging_config

logging = logging_config.setup_logging(__name__)

# Функция для навигации и подготовки страницы
async def prepare_page(page):
    logging.info("Navigating to Deep AI Chat...")
    await page.goto('https://deepai.org/chat', wait_until='domcontentloaded')
    await page.wait_for_selector("#chatSubmitButton", timeout=60000)

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
