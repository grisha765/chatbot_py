from chatbot.config.config import Config
from chatbot.core.browser import init_browser

class Model:
    def __init__(self):
        self.model = str()
        self.text = str()
        self.browser = None
        self.page = None
        self.playwright = None
        self.send_message = None

    async def options(self, model, chrome_path=None):
        if chrome_path:
            Config.chrome_path = chrome_path

        self.browser, self.page, self.playwright = await init_browser()
        if 'duck' in model:
            from chatbot.providers.ddgo.start import prepare_page
            await prepare_page(self.page)
            from chatbot.providers.ddgo.gpt3 import send_message as send_message_gpt3
            from chatbot.providers.ddgo.llama3 import send_message as send_message_llama3
            if model == 'gpt-3.5-duck':
                self.send_message = send_message_gpt3
            elif model == 'llama3-duck':
                self.send_message = send_message_llama3
        elif 'deepai' in model:
            from chatbot.providers.deepai.start import prepare_page
            await prepare_page(self.page)
            from chatbot.providers.deepai.gpt3 import send_message as send_message_gpt3
            self.send_message = send_message_gpt3
        else:
            raise ValueError("Invalid model specified")

    async def send(self, text):
        if self.send_message is None:
            raise ValueError("No send_message function specified")
        response = await self.send_message(self.page, text)
        return response

    async def close(self):
        if self.browser is not None:
            await self.browser.close()
        if self.playwright is not None:
            await self.playwright.stop()

if __name__ == '__main__':
    raise RuntimeError("This module should be run only via main.py")
