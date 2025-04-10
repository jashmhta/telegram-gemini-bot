# Telegram Bot with Gemini Integration

A Telegram bot that uses Google's Gemini AI to respond to user messages.

## Features

- Responds to user messages using Gemini 1.5 Pro AI
- Maintains conversation history for context-aware responses
- Handles long responses by splitting them into multiple messages
- Includes commands for starting, clearing history, and getting help

## Commands

- `/start` - Start or restart the bot and clear conversation history
- `/help` - Display help information
- `/clear` - Clear conversation history

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   TELEGRAM_TOKEN=your_telegram_token
   GEMINI_API_KEY=your_gemini_api_key
   ```
4. Run the bot:
   ```
   python bot.py
   ```

## Deployment

The bot can be deployed on any server with Python installed. For continuous operation, consider using a process manager like `systemd` or `supervisor`.

## License

MIT
