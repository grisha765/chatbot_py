import asyncio
from pyppeteer import launch

import logging_config
logging = logging_config.setup_logging(name='chat_bot', enable_detailed_logs=True)

# Функция для инициализации браузера и страницы
async def init_browser():
    browser = await launch()
    page = await browser.newPage()
    return browser, page

# Функция для навигации и подготовки страницы
async def prepare_page(page):
    logging.info("Navigating to DuckDuckGo AI Chat...")
    await page.goto('https://duckduckgo.com/?q=DuckDuckGo&ia=chat')
    
    # Ждем, пока страница полностью загрузится
    await page.waitForSelector('button')
    
    # Нажимаем на кнопку с текстом "Get Started"
    logging.info("Clicking 'Get Started' button...")
    buttons = await page.querySelectorAll('button')
    for button in buttons:
        text = await page.evaluate('(button) => button.textContent', button)
        if 'Get Started' in text:
            await button.click()
            break
    
    await asyncio.sleep(3)  # ждем 3 секунды

    # Ждем появления кнопки "Next"
    await page.waitForSelector('button')

    # Нажимаем на кнопку с текстом "Next"
    logging.info("Clicking 'Next' button...")
    buttons = await page.querySelectorAll('button')
    for button in buttons:
        text = await page.evaluate('(button) => button.textContent', button)
        if 'Next' in text:
            await button.click()
            break

    await asyncio.sleep(3)  # ждем 3 секунды 

    # Ждем появления кнопки "I Agree"
    await page.waitForSelector('button')

    # Нажимаем на кнопку с текстом "I Agree"
    logging.info("Clicking 'I Agree' button...")
    buttons = await page.querySelectorAll('button')
    for button in buttons:
        text = await page.evaluate('(button) => button.textContent', button)
        if 'I Agree' in text:
            await button.click()
            break

    await asyncio.sleep(3)  # ждем 3 секунды 

# Функция для отправки сообщения и получения ответа
async def send_message(page, message, screenshot_path=None):
    # Ввод текста в поле ввода
    logging.debug(f"Typing text: {message}")
    await page.type('textarea[placeholder="Chat with GPT-3.5"]', message)
    
    # Нажимаем кнопку отправки
    logging.debug("Clicking 'Send' button...")
    send_button = await page.querySelector('button[aria-label="Send"]')
    await send_button.click()
    
    # Динамическое ожидание появления нового ответа
    logging.debug("Waiting for response...")
    last_response = ""
    while True:
        await asyncio.sleep(1)
        response_elements = await page.querySelectorAll('div > div:nth-child(2) > div:nth-child(2)')
        if response_elements:
            current_response = await page.evaluate('(element) => element.innerText', response_elements[-1])
            if current_response != last_response:
                last_response = current_response
            else:
                break
    
    # Печатаем ответ
    print(f"GPT-3.5: {last_response}")

    # Делаем скриншот, если указан путь
    if screenshot_path:
        logging.info(f"Saving screenshot to {screenshot_path}")
        await page.screenshot({'path': screenshot_path})

# Функция для FastAPI, возвращающая ответ без печати
async def send_message_fastapi(page, message):
    # Ввод текста в поле ввода
    logging.info(f"Typing text: {message}")
    await page.type('textarea[placeholder="Chat with GPT-3.5"]', message)
    
    # Нажимаем кнопку отправки
    logging.info("Clicking 'Send' button...")
    send_button = await page.querySelector('button[aria-label="Send"]')
    await send_button.click()
    
    # Динамическое ожидание появления нового ответа
    logging.info("Waiting for response...")
    last_response = ""
    while True:
        await asyncio.sleep(1)
        response_elements = await page.querySelectorAll('div > div:nth-child(2) > div:nth-child(2)')
        if response_elements:
            current_response = await page.evaluate('(element) => element.innerText', response_elements[-1])
            if current_response != last_response:
                last_response = current_response
            else:
                break

    # Нажимаем кнопку очистки
    logging.info("Clicking 'Clear' button...")
    buttons = await page.querySelectorAll('[data-reach-tooltip-trigger]')
    if len(buttons) >= 4:
        await buttons[3].click()
        logging.info("Clicking the second 'Clear' button...")
    else:
        logging.error("The required button was not found.")

    # Возвращаем ответ
    return last_response

# Функция для создания скриншота
async def take_screenshot(page, file_name):
    logging.info(f"Taking screenshot: {file_name}")
    await page.screenshot({'path': file_name})
    print(f"Screenshot saved as {file_name}")

# Основная функция
async def main(input_text=None, screenshot_path=None):
    try:
        browser, page = await init_browser()
        await prepare_page(page)

        # Если введен текст, отправляем его и завершаем
        if input_text:
            await send_message(page, input_text, screenshot_path)
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
                    await send_message(page, user_input)

        # Закрываем браузер
        await browser.close()
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == '__main__':
    raise RuntimeError("This module should be run only via main.py")

