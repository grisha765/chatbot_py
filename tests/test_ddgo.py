from core.init_browser import init_browser
from providers.ddgo.start import prepare_page
from providers.ddgo.gpt3 import send_message
from config.config import Config
from config import logging_config
logging = logging_config.setup_logging(__name__)
async def test_bot_response():
    browser, page = await init_browser()
    try:
        await prepare_page(page)
        response = await send_message(page, Config.test_request)
        assert Config.test_response in response
    except:
        logging.error(f"The bot's response does not contain the word '{Config.test_response}'")
    finally:
        await browser.close()
        logging.info(f'{"\x1b[32m"}Test passed!{"\x1b[0m"}')
