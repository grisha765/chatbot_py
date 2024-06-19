from core.browser import init_browser
from providers.ddgo.start import prepare_page as prepare_page_ddgo
from providers.deepai.start import prepare_page as prepare_page_deepai
from providers.deepai.gpt3 import send_message as send_message_gpt3deepai
from providers.ddgo.gpt3 import send_message as send_message_ddgogpt3
from providers.ddgo.llama3 import send_message as send_message_ddgollama3
from config.config import Config
from config import logging_config
logging = logging_config.setup_logging(__name__)
TEST_MODELS = {
    'gpt-3.5-duck': (send_message_ddgogpt3, prepare_page_ddgo),
    'llama3-duck': (send_message_ddgollama3, prepare_page_ddgo),
    'gpt-3.5-deepai': (send_message_gpt3deepai, prepare_page_deepai)
}

async def test_bot_response():
    for model, (send_message_func, prepare_page_func) in TEST_MODELS.items():
        browser, page, playwright = await init_browser()
        try:
            await prepare_page_func(page)
            response = await send_message_func(page, Config.test_request)
            assert Config.test_response in response
            logging.info(f'{"\x1b[32m"}{model}: Test passed!{"\x1b[0m"}')
        except AssertionError:
            logging.warning(f'{"\x1b[31m"}{model}: Test failed. Response does not contain "{Config.test_response}".{"\x1b[0m"}')
        except Exception as e:
            logging.error(f'{"\x1b[31m"}{model}: An error occurred: {e}{"\x1b[0m"}')
        finally:
            await browser.close()
            await playwright.stop()

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
