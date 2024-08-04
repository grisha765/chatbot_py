# chatbot_py

This project provides an implementation of a chatbot that interacts with various GPT-based models through a FastAPI interface and a script for command-line interactions.

### Initial Setup

1. **Clone the repository**: Clone this repository using `git clone`.
2. **Create Virtual Env**: Create a Python Virtual Environment `venv` to download the required dependencies and libraries.
3. **Download Dependencies**: Download the required dependencies into the Virtual Environment `venv` using `pip`.

```shell
git clone https://github.com/grisha765/chatbot_py.git
cd chatbot_py
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Usage

You can either run the FastAPI server or interact with the chatbot directly from the command line.

### Running interactive mode.

- To start the interactive mode, use the following command:
    ```bash
    python -m chatbot --model gpt-3.5-duck
    ```

### Running the FastAPI Server

- To start the FastAPI server, use the following command:
    ```bash
    python -m chatbot --api
    ```

***This will start the server on `127.0.0.1:8000`.***

### Interacting with the Chatbot

To interact with the chatbot directly from the command line, use:

- One message:
    ```bash
    python -m chatbot --model gpt-3.5-duck "Your message here"
    ```

- To save a screenshot of the interaction, use:
    ```bash
    python -m chatbot --model gpt-3.5-duck "Your message here" --screenshot "path/to/screenshot.png"
    ```

### Python library

- Install with pip
    ```bash
    pip install git+https://github.com/grisha765/chatbot_py.git@main#egg=chatbot
    ```

- Use as python lib.
    ```python
    # import libs
    import asyncio, chatbot

    # use async func
    async def main():
        # init model class
        model = chatbot.Model()
        # set options
        await model.options(model='gpt-3.5-duck', chrome_path='/usr/bin/chromium')
        # send message to chatbot
        response = await model.send("Hello, world!")
        # print response
        print(response)
        # close model
        await model.close()

    if __name__ == "__main__":
        # run async func
        asyncio.run(main())
    ```

## API Endpoints

### POST /v1/chat/completions

- Request:
    ```json
    {
      "model": "gpt-3.5-duck",
      "messages": [
        {"role": "user", "content": "Hello, GPT-3.5!"}
      ],
      "temperature": 0.5
    }
    ```

- Response:
    ```json
    {
        "id": "chatcmpl-12345",
        "object": "chat.completion",
        "created": 1677631234,
        "model": "model",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "response"
                },
                "finish_reason": "stop"
            }
        ]
    }
    ```

- Headers:

- `Authorization: Bearer <API_KEY>`

- Curl request:
    ```bash
    curl http://127.0.0.1:8000/v1/chat/completions \
             -H "Content-Type: application/json" \
             -H "Authorization: Bearer adminapi007" \
             -d '{
            "model": "gpt-3.5-duck",
            "messages": [{"role": "user", "content": "Hello World!"}],
            "temperature": 0.7
          }'
    ```

- Use in python:
    ```python
    import requests # pip install requests
    import json

    text = 'Hello World!'
    url = "http://127.0.0.1:8000/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer adminapi007"
    }
    data = {
        "model": "gpt-3.5-duck",
        "messages": [{"role": "user", "content": f"{text}"}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        message = response_data['choices'][0]['message']['content']
        print("Message:", message)
    else:
        print("Failed to get response:", response.status_code)
    ```

## Features

- **Browser Automation**: Utilizes pyppeteer to automate browser interactions, simulating user actions to chat with the GPT model.
- **Interactive Mode**: Provides an interactive mode for chatting directly via the command line, with special commands for taking screenshots.
- **API Key Authentication**: Secure API endpoint with key-based authentication for authorized access.
- **Error Handling**: Robust error handling to manage and log exceptions during execution.
- **Configurable Settings**: Easily adjustable settings for logging details and API configurations.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.
