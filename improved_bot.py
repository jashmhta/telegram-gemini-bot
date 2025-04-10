#!/usr/bin/env python3
"""
Improved Telegram Bot with Gemini Integration
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

# Configure logging - more verbose for debugging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Changed to DEBUG for more detailed logs
)
logger = logging.getLogger(__name__)

# Get tokens from environment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Log token availability (not the actual tokens)
logger.info(f"Telegram Token available: {TELEGRAM_TOKEN is not None}")
logger.info(f"Gemini API Key available: {GEMINI_API_KEY is not None}")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Try to list available models for debugging
try:
    models = genai.list_models()
    logger.info("Available Gemini models:")
    for model in models:
        logger.info(f"- {model.name}")
except Exception as e:
    logger.error(f"Error listing models: {e}")

# Initialize Gemini model - trying a different model that might be more stable
try:
    # Try gemini-1.0-pro first as it might be more stable
    model = genai.GenerativeModel('models/gemini-1.0-pro')
    logger.info("Using models/gemini-1.0-pro")
except Exception as e:
    logger.error(f"Error initializing gemini-1.0-pro: {e}")
    try:
        # Fall back to gemini-1.5-flash if pro isn't available
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        logger.info("Using models/gemini-1.5-flash")
    except Exception as e:
        logger.error(f"Error initializing gemini-1.5-flash: {e}")
        # Last resort, try the original model
        model = genai.GenerativeModel('models/gemini-1.5-pro')
        logger.info("Using models/gemini-1.5-pro")

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    logger.info(f"Start command received from user {user.id}")
    await update.message.reply_text(
        f"Hi {user.first_name}! I'm a Gemini powered bot. Ask me anything!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    logger.info(f"Help command received from user {update.effective_user.id}")
    help_text = """
I'm a Telegram bot powered by Gemini. Here's how you can use me:

- Just send me any message and I'll respond using Gemini
- Use /start to restart our conversation
- Use /help to see this help message
- Try simple questions or calculations first

Feel free to ask me anything!
    """
    await update.message.reply_text(help_text)

# Message handler - with improved error handling
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process user messages and respond using Gemini."""
    user_id = update.effective_user.id
    user_message = update.message.text
    
    logger.info(f"Message received from user {user_id}: {user_message}")
    
    try:
        # Send "typing..." action
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Add safety measures for the API call
        generation_config = {
            'temperature': 0.7,
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 1024,  # Reduced for stability
        }
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
        
        logger.debug(f"Sending request to Gemini API: {user_message}")
        
        # Simple direct request to Gemini without conversation history
        response = model.generate_content(
            user_message,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # Get the response text
        response_text = response.text
        logger.debug(f"Received response from Gemini API: {response_text[:100]}...")
        
        # Send response back to user (split if too long)
        if len(response_text) > 4096:
            # Split response into chunks of 4096 characters (Telegram's limit)
            chunks = [response_text[i:i+4096] for i in range(0, len(response_text), 4096)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(response_text)
        
    except Exception as e:
        error_message = str(e)
        logger.error(f"Error generating response: {error_message}")
        
        # Send a more helpful error message to the user
        if "safety" in error_message.lower():
            await update.message.reply_text(
                "I'm unable to respond to this message due to safety settings. Please try a different question."
            )
        elif "rate limit" in error_message.lower():
            await update.message.reply_text(
                "I've received too many requests. Please wait a moment before trying again."
            )
        else:
            await update.message.reply_text(
                f"Sorry, I encountered an error: {error_message[:100]}...\n\nPlease try a simpler question or try again later."
            )

def main() -> None:
    """Start the bot."""
    logger.info("Starting the bot")
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    logger.info("Starting polling")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
