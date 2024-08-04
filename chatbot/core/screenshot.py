import os
from chatbot.config import logging_config
logging = logging_config.setup_logging(__name__)

# Функция для создания скриншота
async def take_screenshot(page, file_name):
    logging.info(f"Taking screenshot: {file_name}")
    await page.screenshot(path=file_name)
    print(f"Screenshot saved as {file_name}")
    os.system(f"feh {file_name}")
