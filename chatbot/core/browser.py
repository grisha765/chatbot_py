from playwright.async_api import async_playwright
from chatbot.config.config import Config
# Функция для инициализации браузера и страницы
async def init_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(executable_path=Config.chrome_path)
    page = await browser.new_page()
    return browser, page, playwright

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")

