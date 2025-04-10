#!/usr/bin/env python3
"""
GitHub Repository Update Script
This script updates the Telegram bot repository with the OpenAI version.
"""

import os
import subprocess
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get GitHub PAT from environment variables
GITHUB_PAT = os.getenv('GITHUB_PAT')

def get_user_info():
    """Get GitHub user information."""
    headers = {
        'Authorization': f'token {GITHUB_PAT}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get('https://api.github.com/user', headers=headers)
    
    if response.status_code == 200:
        return response.json()['login']
    else:
        print(f"Failed to get user info. Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        return None

def update_repository(username, repo_name):
    """Update the repository with the OpenAI version of the bot."""
    try:
        # Create the remote URL with embedded PAT
        remote_url = f'https://{GITHUB_PAT}@github.com/{username}/{repo_name}.git'
        
        # Check if git is already initialized
        if not os.path.exists('.git'):
            print("Initializing git repository...")
            subprocess.run(['git', 'init'], check=True)
        else:
            print("Git repository already initialized.")
        
        # Update .gitignore file
        with open('.gitignore', 'w') as f:
            f.write(".env\n__pycache__/\n*.py[cod]\n*$py.class\n.venv/\nvenv/\nENV/\n")
        
        # Configure git user (required for commit)
        subprocess.run(['git', 'config', 'user.email', 'bot@example.com'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'Telegram Bot Deployer'], check=True)
        
        # Check if remote origin exists
        result = subprocess.run(['git', 'remote'], capture_output=True, text=True)
        if 'origin' in result.stdout:
            print("Removing existing remote origin...")
            subprocess.run(['git', 'remote', 'remove', 'origin'], check=True)
        
        # Add remote origin with PAT embedded in URL
        print("Adding remote origin...")
        subprocess.run(['git', 'remote', 'add', 'origin', remote_url], check=True)
        
        # Add all files to git
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit changes
        subprocess.run(['git', 'commit', '-m', 'Update: Added OpenAI version of Telegram bot'], check=True)
        
        # Force push to GitHub to overwrite any existing content
        print("Pushing to GitHub...")
        subprocess.run(['git', 'push', '-u', 'origin', 'master', '--force'], check=True)
        
        print("Repository successfully updated with OpenAI bot!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during git operations: {e}")
        return False

def update_readme():
    """Update README.md file to include OpenAI bot information."""
    readme_content = """# Telegram Bot with AI Integration

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
"""
    with open('README.md', 'w') as f:
        f.write(readme_content)
    print("README.md updated successfully!")

def update_requirements():
    """Update requirements.txt file to include OpenAI dependencies."""
    with open('requirements.txt', 'w') as f:
        f.write("python-telegram-bot>=22.0\ngoogle-generativeai>=0.8.0\nopenai>=1.0.0\nrequests>=2.28.0\npython-dotenv>=1.0.0\n")
    print("requirements.txt updated successfully!")

def main():
    """Main function to update GitHub repository."""
    repo_name = "telegram-gemini-bot"
    
    # Update README.md
    update_readme()
    
    # Update requirements.txt
    update_requirements()
    
    # Get GitHub username
    username = get_user_info()
    
    if username:
        print(f"Using GitHub account: {username}")
        print(f"Repository: {username}/{repo_name}")
        
        # Update repository
        if update_repository(username, repo_name):
            repo_url = f"https://github.com/{username}/{repo_name}"
            print(f"Repository update complete! Repository URL: {repo_url}")
            return repo_url
        else:
            print("Failed to update repository.")
    else:
        print("Failed to get GitHub user information. Check your PAT.")
    
    return None

if __name__ == "__main__":
    main()
