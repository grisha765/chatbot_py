from core.init_browser import init_browser
from providers.ddgo.start import prepare_page
from providers.ddgo.gpt3 import send_message as send_message_gpt3
from providers.ddgo.llama3 import send_message as send_message_llama3
from config.config import Config
from config import logging_config
logging = logging_config.setup_logging(__name__)
TEST_MODELS = {
    'gpt-3.5-duck': send_message_gpt3,
    'llama3-duck': send_message_llama3
}

async def test_bot_response():
    for model, send_message_func in TEST_MODELS.items():
        browser, page = await init_browser()
        try:
            await prepare_page(page)
            response = await send_message_func(page, Config.test_request)
            assert Config.test_response in response
            logging.info(f'{"\x1b[32m"}{model}: Test passed!{"\x1b[0m"}')
        except AssertionError:
            logging.error(f'{"\x1b[31m"}{model}: Test failed. Response does not contain "{Config.test_response}".{"\x1b[0m"}')
        except Exception as e:
            logging.error(f'{"\x1b[31m"}{model}: An error occurred: {e}{"\x1b[0m"}')
        finally:
            await browser.close()
