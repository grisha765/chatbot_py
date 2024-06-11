from core.init_browser import init_browser
from providers.ddgo.start import prepare_page
from providers.ddgo.gpt3 import send_message
from config import logging_config
logging = logging_config.setup_logging(__name__)

async def test_bot_response():
    input_text = "Напиши мне слово Тест и ничего более!"
    
    browser, page = await init_browser()
    try:
        await prepare_page(page)
        response = await send_message(page, input_text)
        assert "Тест" in response
    except:
        logging.error("The bot's response does not contain the word 'Тест'")
    finally:
        await browser.close()
        logging.info("Test passed!")

