from tests.test_ddgo import test_bot_response
from config import logging_config
async def run():
    logging = logging_config.setup_logging(__name__)
    try:
        logging.info("Start tests...")
        await test_bot_response()
    except Exception as e:
        logging.error(f"An error occurred during test execution: {e}")
    else:
        logging.info("All tests passed!")
