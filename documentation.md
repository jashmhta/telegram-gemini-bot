# Telegram Bot with Gemini Integration - Documentation

## Overview

This Telegram bot integrates with Google's Gemini AI to provide intelligent responses to user messages. The bot maintains conversation history for context-aware interactions and supports several commands for user convenience.

## Features

- **AI-Powered Responses**: Uses Google's Gemini 1.5 Pro model to generate intelligent, contextual responses
- **Conversation Memory**: Maintains conversation history for each user to provide context-aware responses
- **Command Support**: Includes commands for starting conversations, clearing history, and getting help
- **Long Response Handling**: Automatically splits long responses to comply with Telegram's message length limits

## Commands

- `/start` - Initiates or restarts the bot, clearing any existing conversation history
- `/help` - Displays help information about the bot's capabilities and commands
- `/clear` - Clears the current conversation history to start fresh

## Technical Details

### Architecture

The bot is built using:
- **Python 3.10+**: Core programming language
- **python-telegram-bot 22.0+**: Framework for interacting with the Telegram Bot API
- **google-generativeai 0.8.0+**: Google's official SDK for accessing Gemini AI models
- **python-dotenv**: For managing environment variables and API keys

### Configuration

The bot uses environment variables stored in a `.env` file:
- `TELEGRAM_TOKEN`: Your Telegram bot token obtained from BotFather
- `GEMINI_API_KEY`: Your Google Gemini API key

### AI Model

The bot uses the `models/gemini-1.5-pro` model with the following configuration:
- Temperature: 0.7 (controls randomness)
- Top-p: 0.95 (nucleus sampling parameter)
- Top-k: 40 (limits vocabulary to top K options)
- Max output tokens: 2048 (maximum response length)

### Conversation Management

- Each user's conversation history is stored in memory
- The bot maintains the last 10 exchanges (20 messages) to stay within token limits
- A system prompt guides the AI's behavior and sets expectations

## Security Considerations

- API keys should be kept secure and not shared publicly
- The `.env` file is excluded from version control via `.gitignore`
- Consider implementing user authentication for sensitive applications

## Limitations

- The bot runs as long as the script is active; for 24/7 operation, use a process manager
- Conversation history is stored in memory and will be lost if the bot restarts
- Token limits may restrict very long conversations

## Future Enhancements

Potential improvements for future versions:
- Persistent storage for conversation history (database integration)
- Media handling capabilities (images, audio, documents)
- User preference settings
- Multi-language support
- Integration with additional AI models or services
