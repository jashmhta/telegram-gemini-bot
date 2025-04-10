# Telegram Bot with Gemini Integration - Deployment Instructions

This document provides instructions for deploying and running your Telegram bot with Gemini integration.

## Files Overview

- `bot.py` - The main bot script that integrates Telegram with Gemini
- `.env` - Environment file containing your API keys (keep this secure)
- `requirements.txt` - List of Python dependencies

## Deployment Options

### Option 1: Run Locally

1. Ensure Python 3.8+ is installed on your system
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Make sure your `.env` file contains the correct API keys:
   ```
   TELEGRAM_TOKEN=your_telegram_token
   GEMINI_API_KEY=your_gemini_api_key
   ```
4. Run the bot:
   ```
   python bot.py
   ```
5. The bot will run as long as the script is active. For continuous operation, consider using a process manager like `systemd`, `supervisor`, or `pm2`.

### Option 2: Deploy on a VPS or Cloud Server

1. Set up a VPS or cloud server (AWS, DigitalOcean, Linode, etc.)
2. Install Python 3.8+ on the server
3. Upload the bot files to the server
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Set up a process manager to keep the bot running:

   **Using Systemd (Linux):**
   
   Create a service file at `/etc/systemd/system/telegram-bot.service`:
   ```
   [Unit]
   Description=Telegram Bot with Gemini Integration
   After=network.target

   [Service]
   User=your_username
   WorkingDirectory=/path/to/bot/directory
   ExecStart=/usr/bin/python3 /path/to/bot/directory/bot.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable and start the service:
   ```
   sudo systemctl enable telegram-bot
   sudo systemctl start telegram-bot
   ```

### Option 3: Deploy on PythonAnywhere

1. Sign up for a PythonAnywhere account
2. Upload your bot files
3. Set up a virtual environment and install dependencies
4. Create a new "Always-on task" that runs your bot script

## Troubleshooting

- **Bot not responding:** Check that your Telegram token is correct and the bot is running
- **Gemini API errors:** Verify your API key and check that you're using a supported model
- **Connection issues:** Ensure your server has internet access and can reach the Telegram and Gemini APIs

## Maintenance

- Periodically check for updates to the python-telegram-bot and google-generativeai libraries
- Monitor your bot's performance and adjust the conversation history limits if needed
- Keep your API keys secure and rotate them periodically

## Additional Resources

- [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/)
- [Google Generative AI Python SDK](https://github.com/google/generative-ai-python)
- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
