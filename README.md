# Telegram Bot with AI Integration

A Telegram bot that uses AI to respond to user messages.

## Features

- Responds to user messages using AI (OpenAI or Gemini)
- Maintains conversation history for context-aware responses
- Handles long responses by splitting them into multiple messages
- Includes commands for starting, clearing history, and getting help

## Versions

This repository contains two versions of the bot:

### 1. Gemini Version (bot.py)

Uses Google's Gemini API for responses. May be subject to rate limiting on the free tier.

### 2. OpenAI Version (openai_bot.py)

Uses OpenAI's API for responses. Generally has higher rate limits and more stable performance.

## Commands

- `/start` - Start or restart the bot and clear conversation history
- `/help` - Display help information
- `/clear` - Clear conversation history

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install python-telegram-bot google-generativeai openai requests python-dotenv
   ```
3. Create a `.env` file with your API keys:
   ```
   TELEGRAM_TOKEN=your_telegram_token
   GEMINI_API_KEY=your_gemini_api_key  # For Gemini version
   OPENAI_API_KEY=your_openai_api_key  # For OpenAI version
   ```
4. Run the bot:
   ```
   python bot.py  # For Gemini version
   # OR
   python openai_bot.py  # For OpenAI version
   ```

## Deployment

The bot can be deployed on any server with Python installed. For continuous operation, consider using a process manager like `systemd` or `supervisor`.

## License

MIT
