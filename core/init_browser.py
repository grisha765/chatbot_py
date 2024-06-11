from pyppeteer import launch

from providers.ddgo.start import prepare_page
from providers.ddgo.gpt3 import send_message as send_message_gpt3
from providers.ddgo.llama3 import send_message as send_message_llama3
from core.screenshot import take_screenshot
from config import logging_config
logging = logging_config.setup_logging(__name__)

# Функция для инициализации браузера и страницы
async def init_browser():
    browser = await launch()
    page = await browser.newPage()
    return browser, page

# Основная функция
async def main(input_text=None, screenshot_path=None, model=None):
    try:
        browser, page = await init_browser()
        await prepare_page(page)

        if model == 'gpt-3.5-duck':
            send_message = send_message_gpt3
        elif model == 'llama3-duck':
            send_message = send_message_llama3
        else:
            raise ValueError("Invalid model specified")

        # Если введен текст, отправляем его и завершаем
        if input_text:
            response = await send_message(page, input_text, screenshot_path)
            print(response)
        else:
            # Иначе запускаем интерактивный режим
            print("Entering interactive chat mode. Type 'exit' to quit.")
            while True:
                user_input = input("You: ")
                if user_input.lower() == 'exit':
                    break
                elif user_input.startswith('/screen'):
                    _, file_name = user_input.split(maxsplit=1)
                    await take_screenshot(page, file_name)
                else:
                    response = await send_message(page, user_input)
                    print(f"Bot: {response}")
        # Закрываем браузер
        await browser.close()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
if __name__ == '__main__':
    raise RuntimeError("This module should be run only via main.py")
