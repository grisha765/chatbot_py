import argparse
import asyncio
import signal
import uvicorn

from core.init_browser import main as browser_main
from tests.run import run
from config.config import Config
from config import logging_config

def handle_exit(sig, frame):
    logging.info("Shutting down server...")
    asyncio.get_event_loop().stop()

def run_api():
    logging.info("Starting FastAPI server...")
    config = uvicorn.Config("core.api:app", host=Config.api_host, port=Config.api_port, log_level="info")
    server = uvicorn.Server(config)

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, handle_exit, signal.SIGINT, None)
    loop.add_signal_handler(signal.SIGTERM, handle_exit, signal.SIGTERM, None)

    asyncio.ensure_future(server.serve())
    loop.run_forever()

def run_chat_bot(input_text=None, screenshot_path=None, model=None):
    logging.info("Starting Chat Bot...")
    response = asyncio.run(browser_main(input_text, screenshot_path, model))
    return response

async def run_tests():
    await run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Project launcher for FastAPI and Chat Bot")
    parser.add_argument('--api', action='store_true', help='Run the FastAPI server')
    parser.add_argument('input_text', type=str, nargs='?', default=None, help='Text to send to the Chat Bot')
    parser.add_argument('--screenshot', type=str, default='', help='Path to save screenshot (optional)')
    parser.add_argument('--tests',nargs='?', const=True, default=False, help='Run tests...')
    parser.add_argument('--model', type=str, choices=['gpt-3.5-duck', 'llama3-duck'], help='Model to use for the chat bot')
    args = parser.parse_args()

    logging = logging_config.setup_logging(__name__)

    if args.api:
        run_api()
    if args.tests:
        asyncio.run(run_tests()) 
    else:
        run_chat_bot(args.input_text, args.screenshot, args.model)

