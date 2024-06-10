import argparse
import asyncio
import signal
import uvicorn

from chat_bot import main as chat_bot_main

import logging_config
logging = logging_config.setup_logging(name='main', enable_detailed_logs=True)

def handle_exit(sig, frame):
    logging.info("Shutting down server...")
    asyncio.get_event_loop().stop()

def run_api():
    logging.info("Starting FastAPI server...")
    config = uvicorn.Config("api:app", host="127.0.0.1", port=8000, log_level="info")
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

    if args.api:
        run_api()
    else:
        run_chat_bot(args.input_text, args.screenshot)

