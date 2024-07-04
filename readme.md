# Chad Tournament

This project runs a tournament to determine the ultimate "Chad" in a given theme using OpenAI's GPT model.

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your OpenAI API key in the system keyring:

python -c "import keyring; keyring.set_password('system', 'openai_api_key', 'your-api-key-here')"

## Configuration

Adjust the OpenAI model and other settings in `config/config.json`.

## Cache

The cache is stored in `data/chad_cache.json` and is organized by theme for easy reading and maintenance.

## Logs

Logs are stored in `logs/chad_tournament.log`.