#!/usr/bin/env python3
"""
Telegram Bot with OpenAI Integration
This bot uses the OpenAI API to respond to user messages on Telegram.
"""

import os
import logging
import openai
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
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # New environment variable for OpenAI

# Configure OpenAI API
openai.api_key = OPENAI_API_KEY

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hi {user.first_name}! I'm an AI-powered bot. Ask me anything!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
I'm a Telegram bot powered by OpenAI. Here's how you can use me:

- Just send me any message and I'll respond
- Use /start to restart our conversation
- Use /help to see this help message
- Use /clear to clear our conversation history

Feel free to ask me anything!
    """
    await update.message.reply_text(help_text)

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear the conversation history when the command /clear is issued."""
    user_id = update.effective_user.id
    if 'conversation_history' in context.user_data:
        context.user_data['conversation_history'] = []
    await update.message.reply_text("Conversation history cleared. Let's start fresh!")

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process user messages and respond using OpenAI."""
    user_id = update.effective_user.id
    user_message = update.message.text
    
    # Initialize conversation history if it doesn't exist
    if 'conversation_history' not in context.user_data:
        context.user_data['conversation_history'] = []
    
    try:
        # Send "typing..." action
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Prepare conversation history for OpenAI
        messages = [{"role": "system", "content": "You are a helpful, friendly, and knowledgeable assistant."}]
        
        # Add conversation history (limited to last 10 exchanges to manage token usage)
        for msg in context.user_data['conversation_history'][-10:]:
            messages.append(msg)
        
        # Add the current user message
        messages.append({"role": "user", "content": user_message})
        
        # Get response from OpenAI
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # You can change this to other models like "gpt-4" if available
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        
        # Extract the response text
        response_text = response.choices[0].message.content
        
        # Update conversation history
        context.user_data['conversation_history'].append({"role": "user", "content": user_message})
        context.user_data['conversation_history'].append({"role": "assistant", "content": response_text})
        
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
            f"Sorry, I encountered an error while processing your request: {str(e)[:100]}...\n\nPlease try again later."
        )

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
