#!/usr/bin/env python3
"""
Telegram Bot with Gemini Integration
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

# Create a conversation history dictionary to store chat history for each user
conversation_history = {}

# Initialize Gemini model with enhanced parameters
# Using models/gemini-1.5-pro which is available in the API
model = genai.GenerativeModel(
    model_name='models/gemini-1.5-pro',
    generation_config={
        'temperature': 0.7,
        'top_p': 0.95,
        'top_k': 40,
        'max_output_tokens': 2048,
    }
)

# System prompt to guide the model's behavior
SYSTEM_PROMPT = """
You are a helpful, friendly, and knowledgeable assistant powered by Gemini.
Your responses should be informative, engaging, and accurate.
If you're unsure about something, acknowledge your uncertainty rather than providing incorrect information.
Be respectful, avoid harmful content, and maintain a conversational tone.
"""

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    user_id = update.effective_user.id
    
    # Reset conversation history for this user
    conversation_history[user_id] = []
    
    await update.message.reply_text(
        f"Hi {user.first_name}! I'm a Gemini powered bot. Ask me anything!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
I'm a Telegram bot powered by Gemini. Here's how you can use me:

- Just send me any message and I'll respond using Gemini
- Use /start to restart our conversation and clear chat history
- Use /help to see this help message
- Use /clear to clear our conversation history

Feel free to ask me anything!
    """
    await update.message.reply_text(help_text)

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear the conversation history when the command /clear is issued."""
    user_id = update.effective_user.id
    conversation_history[user_id] = []
    await update.message.reply_text("Conversation history cleared. Let's start fresh!")

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process user messages and respond using Gemini with conversation history."""
    user_id = update.effective_user.id
    user_message = update.message.text
    
    # Initialize conversation history for new users
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    try:
        # Send "typing..." action
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Prepare conversation for Gemini
        chat = model.start_chat(history=[])
        
        # Add system prompt if this is a new conversation
        if not conversation_history[user_id]:
            chat.send_message(SYSTEM_PROMPT)
        
        # Add conversation history
        for message in conversation_history[user_id]:
            chat.send_message(message)
        
        # Send user message and get response
        response = chat.send_message(user_message)
        response_text = response.text
        
        # Update conversation history (keep last 10 messages to avoid token limits)
        conversation_history[user_id].append(user_message)
        conversation_history[user_id].append(response_text)
        if len(conversation_history[user_id]) > 20:  # Keep last 10 exchanges (20 messages)
            conversation_history[user_id] = conversation_history[user_id][-20:]
        
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
            "Sorry, I encountered an error while processing your request. Please try again later."
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
