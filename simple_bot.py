#!/usr/bin/env python3
"""
Simplified Telegram Bot with Gemini Integration
This bot uses the Gemini API to respond to user messages on Telegram.
"""

import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get tokens from environment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model - using a simpler configuration
model = genai.GenerativeModel('models/gemini-1.5-pro')

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hi {user.first_name}! I'm a Gemini powered bot. Ask me anything!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
I'm a Telegram bot powered by Gemini. Here's how you can use me:

- Just send me any message and I'll respond using Gemini
- Use /start to restart our conversation
- Use /help to see this help message

Feel free to ask me anything!
    """
    await update.message.reply_text(help_text)

# Message handler - simplified without conversation history
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process user messages and respond using Gemini."""
    user_message = update.message.text
    
    try:
        # Send "typing..." action
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Simple direct request to Gemini without conversation history
        response = model.generate_content(user_message)
        
        # Get the response text
        response_text = response.text
        
        # Send response back to user (split if too long)
        if len(response_text) > 4096:
            # Split response into chunks of 4096 characters (Telegram's limit)
            chunks = [response_text[i:i+4096] for i in range(0, len(response_text), 4096)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(response_text)
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        await update.message.reply_text(
            f"Sorry, I encountered an error while processing your request: {str(e)}"
        )

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
