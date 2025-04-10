#!/usr/bin/env python3
"""
GitHub Repository Setup Script (Fixed)
This script creates a GitHub repository and pushes the Telegram bot code to it.
"""

import os
import subprocess
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get GitHub PAT from environment variables
GITHUB_PAT = os.getenv('GITHUB_PAT')

def create_github_repo(repo_name, description):
    """Create a new GitHub repository."""
    headers = {
        'Authorization': f'token {GITHUB_PAT}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'name': repo_name,
        'description': description,
        'private': False,
        'auto_init': False
    }
    
    response = requests.post('https://api.github.com/user/repos', headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"Repository '{repo_name}' created successfully!")
        return response.json()['html_url']
    else:
        print(f"Failed to create repository. Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        return None

def setup_git_and_push(repo_url):
    """Initialize git repository and push code to GitHub."""
    try:
        # Initialize git repository
        subprocess.run(['git', 'init'], check=True)
        
        # Create .gitignore file
        with open('.gitignore', 'w') as f:
            f.write(".env\n__pycache__/\n*.py[cod]\n*$py.class\n.venv/\nvenv/\nENV/\n")
        
        # Add files to git
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Configure git user (required for commit)
        subprocess.run(['git', 'config', 'user.email', 'bot@example.com'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'Telegram Bot Deployer'], check=True)
        
        # Commit changes
        subprocess.run(['git', 'commit', '-m', 'Initial commit: Telegram bot with Gemini 2.5 Pro integration'], check=True)
        
        # Extract username and repo name from repo_url
        # Example: https://github.com/username/repo-name
        parts = repo_url.split('/')
        username = parts[-2]
        repo_name = parts[-1]
        
        # Create the remote URL with embedded PAT
        remote_url = f'https://{GITHUB_PAT}@github.com/{username}/{repo_name}.git'
        
        # Add remote origin with PAT embedded in URL
        subprocess.run(['git', 'remote', 'add', 'origin', remote_url], check=True)
        
        # Push to GitHub
        subprocess.run(['git', 'push', '-u', 'origin', 'master'], check=True)
        
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
    description = "A Telegram bot powered by Google's Gemini 2.5 Pro API"
    
    # Create README.md
    create_readme()
    
    # Create requirements.txt
    create_requirements_file()
    
    # Create GitHub Actions workflow file
    create_workflow_file()
    
    # Create GitHub repository
    repo_url = create_github_repo(repo_name, description)
    
    if repo_url:
        # Setup git and push code
        if setup_git_and_push(repo_url):
            print(f"Deployment setup complete! Repository URL: {repo_url}")
            return repo_url
    
    return None

if __name__ == "__main__":
    main()
