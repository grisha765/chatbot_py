from tests.test_ddgo import test_bot_response
from tests.test_fastapi import test_chat_completions
from config import logging_config
async def run():
    logging = logging_config.setup_logging(__name__)
    try:
        logging.info(f'{"\x1b[32m"}Start tests...{"\x1b[0m"}')
        await test_bot_response()
        await test_chat_completions()
    except Exception as e:
        logging.error(f"An error occurred during test execution: {e}")
    else:
        logging.info(f'{"\x1b[32m"}All tests passed!{"\x1b[0m"}')
