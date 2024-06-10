# Chatbot_py

This project provides an implementation of a chatbot that interacts with various GPT-based models through a FastAPI interface and a script for command-line interactions.

## Features

- Communicate with GPT models using a web-based interface.
- FastAPI server for API interactions.
- Screenshot functionality for saving chat interactions.
- Detailed logging.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/grisha765/chatbot_py.git
    ```
2. Navigate to the project directory:
    ```bash
    cd chatbot_py
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

You can either run the FastAPI server or interact with the chatbot directly from the command line.

### Running interactive mode.

To start the interactive mode, use the following command:

```bash
python main.py
```

### Running the FastAPI Server

To start the FastAPI server, use the following command:

```bash
python main.py --api
```

This will start the server on `127.0.0.1:8000`.

### Interacting with the Chatbot

To interact with the chatbot directly from the command line, use:

- One message:
    ```bash
    python main.py "Your message here"
    ```

- To save a screenshot of the interaction, use:
    ```bash
    python main.py "Your message here" --screenshot "path/to/screenshot.png"
    ```

## API Endpoints

### POST /v1/chat/completions

**Request:**

```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {"role": "user", "content": "Hello, GPT-3.5!"}
  ],
  "temperature": 0.5
}
```

**Response:**

```json
{
  "response": "Hello! How can I assist you today?"
}
```

**Headers:**

- `Authorization: Bearer <API_KEY>`

**Curl request:**

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

## Project Structure

- `main.py`: Entry point of the application. Contains logic for running the FastAPI server and command-line interactions.
- `api.py`: FastAPI application that handles API requests and interactions with the chatbot.
- `chat_bot.py`: Core chatbot logic including browser automation, message handling, and screenshot functionality.
- `logging_config.py`: Logging configuration.
- `requirements.txt`: List of dependencies.

## Features

- **Browser Automation**: Utilizes `pyppeteer` to automate browser interactions, simulating user actions to chat with the GPT model.
- **Interactive Mode**: Provides an interactive mode for chatting directly via the command line, with special commands for taking screenshots.
- **API Key Authentication**: Secure API endpoint with key-based authentication for authorized access.
- **Error Handling**: Robust error handling to manage and log exceptions during execution.
- **Configurable Settings**: Easily adjustable settings for logging details and API configurations.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.
