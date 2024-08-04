from chatbot.core.screenshot import take_screenshot
from chatbot.core.browser import init_browser
from chatbot.config import logging_config
logging = logging_config.setup_logging(__name__)

# Основная функция
async def main(input_text: str, screenshot_path: str, model: str):
    try:
        browser, page, playwright = await init_browser()
        if 'duck' in model:
            from chatbot.providers.ddgo.start import prepare_page
            await prepare_page(page)
            from chatbot.providers.ddgo.gpt3 import send_message as send_message_gpt3
            from chatbot.providers.ddgo.llama3 import send_message as send_message_llama3
            if model == 'gpt-3.5-duck':
                send_message = send_message_gpt3
            elif model == 'llama3-duck':
                send_message = send_message_llama3
        elif 'deepai' in model:
            from chatbot.providers.deepai.start import prepare_page
            await prepare_page(page)
            from chatbot.providers.deepai.gpt3 import send_message as send_message_gpt3
            send_message = send_message_gpt3
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
        await playwright.stop()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
if __name__ == '__main__':
    raise RuntimeError("This module should be run only via main.py")
