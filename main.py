import argparse
import asyncio
import signal
import uvicorn

from core.init_browser import main as chat_bot_main
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

def run_chat_bot(input_text=None, screenshot_path=None):
    logging.info("Starting Chat Bot...")
    asyncio.run(chat_bot_main(input_text, screenshot_path))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Project launcher for FastAPI and Chat Bot")
    parser.add_argument('--api', action='store_true', help='Run the FastAPI server')
    parser.add_argument('input_text', type=str, nargs='?', default=None, help='Text to send to the Chat Bot')
    parser.add_argument('--screenshot', type=str, default='', help='Path to save screenshot (optional)')
    args = parser.parse_args()

    logging = logging_config.setup_logging(__name__)

    if args.api:
        run_api()
    else:
        run_chat_bot(args.input_text, args.screenshot)

