#!/usr/bin/env python3
"""
GitHub Repository Setup Script (Final Fix)
This script pushes the Telegram bot code to an existing GitHub repository.
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
        return None

def setup_git_and_push(username, repo_name):
    """Initialize git repository and push code to GitHub."""
    try:
        # Create the remote URL with embedded PAT
        remote_url = f'https://{GITHUB_PAT}@github.com/{username}/{repo_name}.git'
        
        # Check if remote origin exists and update it
        result = subprocess.run(['git', 'remote'], capture_output=True, text=True)
        if 'origin' in result.stdout:
            print("Remote origin exists, updating URL...")
            subprocess.run(['git', 'remote', 'set-url', 'origin', remote_url], check=True)
        else:
            print("Adding remote origin...")
            subprocess.run(['git', 'remote', 'add', 'origin', remote_url], check=True)
        
        # Add all files to git
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Configure git user (required for commit)
        subprocess.run(['git', 'config', 'user.email', 'bot@example.com'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'Telegram Bot Deployer'], check=True)
        
        # Commit changes
        subprocess.run(['git', 'commit', '-m', 'Update: Telegram bot with Gemini 2.5 Pro integration'], check=True)
        
        # Force push to GitHub to overwrite any existing content
        subprocess.run(['git', 'push', '-u', 'origin', 'master', '--force'], check=True)
        
        print("Code successfully pushed to GitHub!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during git operations: {e}")
        return False

def create_readme():
    """Create a README.md file for the repository."""
    readme_content = """# Telegram Bot with Gemini 2.5 Pro Integration

A Telegram bot that uses Google's Gemini 2.5 Pro API to respond to user messages.

## Features

- Responds to user messages using Gemini 2.5 Pro AI
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
   pip install python-telegram-bot google-generativeai requests python-dotenv
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
"""
    with open('README.md', 'w') as f:
        f.write(readme_content)
    print("README.md created successfully!")

def create_workflow_file():
    """Create GitHub Actions workflow file for CI/CD."""
    os.makedirs('.github/workflows', exist_ok=True)
    
    workflow_content = """name: Deploy Telegram Bot

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install python-telegram-bot google-generativeai requests python-dotenv
    
    - name: Lint with flake8
      run: |
        pip install flake8
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Create .env file
      run: |
        echo "TELEGRAM_TOKEN=${{ secrets.TELEGRAM_TOKEN }}" > .env
        echo "GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }}" >> .env
      env:
        TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
"""
    
    with open('.github/workflows/deploy.yml', 'w') as f:
        f.write(workflow_content)
    print("GitHub Actions workflow file created successfully!")

def create_requirements_file():
    """Create requirements.txt file."""
    with open('requirements.txt', 'w') as f:
        f.write("python-telegram-bot>=22.0\ngoogle-generativeai>=0.8.0\nrequests>=2.28.0\npython-dotenv>=1.0.0\n")
    print("requirements.txt created successfully!")

def main():
    """Main function to set up GitHub repository and push code."""
    repo_name = "telegram-gemini-bot"
    
    # Create README.md
    create_readme()
    
    # Create requirements.txt
    create_requirements_file()
    
    # Create GitHub Actions workflow file
    create_workflow_file()
    
    # Get GitHub username
    username = get_user_info()
    
    if username:
        print(f"Using existing repository: {username}/{repo_name}")
        # Setup git and push code
        if setup_git_and_push(username, repo_name):
            repo_url = f"https://github.com/{username}/{repo_name}"
            print(f"Deployment setup complete! Repository URL: {repo_url}")
            return repo_url
    
    return None

if __name__ == "__main__":
    main()
