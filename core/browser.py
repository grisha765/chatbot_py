from pyppeteer import launch

# Функция для инициализации браузера и страницы
async def init_browser():
    browser = await launch()
    page = await browser.newPage()
    return browser, page

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
