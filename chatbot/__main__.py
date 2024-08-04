import argparse
import asyncio
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot.core.base import main as base_main
from chatbot.core.api import run_server
from chatbot.tests.run import run
from chatbot.config import logging_config
logging = logging_config.setup_logging(__name__)

def run_chat_bot(input_text=None, screenshot_path=None, model=None):
    logging.info("Starting Chat Bot...")
    response = asyncio.run(base_main(input_text, screenshot_path, model))
    return response

async def run_tests():
    await run()

def main():
    parser = argparse.ArgumentParser(description="Project launcher for FastAPI and Chat Bot")
    parser.add_argument('--api', action='store_true', help='Run the FastAPI server')
    parser.add_argument('input_text', type=str, nargs='?', default=None, help='Text to send to the Chat Bot')
    parser.add_argument('--screenshot', type=str, default='', help='Path to save screenshot (optional)')
    parser.add_argument('--tests',nargs='?', const=True, default=False, help='Run tests...')
    parser.add_argument('--model', type=str, choices=['gpt-3.5-duck', 'llama3-duck', 'gpt-3.5-deepai'], help='Model to use for the chat bot')
    args = parser.parse_args()

    if args.api:
        run_server()
    if args.tests:
        asyncio.run(run_tests()) 
    else:
        run_chat_bot(args.input_text, args.screenshot, args.model)

if __name__ == '__main__':
    main()
