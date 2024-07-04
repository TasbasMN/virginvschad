import keyring
from openai import AsyncOpenAI
import json
from pathlib import Path
from typing import List
import logging
import os
import random

# Ensure logs directory exists
log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(exist_ok=True)

# Configure logging
log_file = log_dir / 'chad_tournament.log'
logging.basicConfig(filename=str(log_file), level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config_path = Path(__file__).parent.parent / "config/config.json"
with config_path.open() as f:
    config = json.load(f)
    
    
def get_openai_api_key() -> str:
    return keyring.get_password("system", "openai_api_key")

client = AsyncOpenAI(api_key=get_openai_api_key())

async def generate_entities(n: int, theme: str, cache) -> List[str]:
    cache_key = f"generate_{n}"
    cached_result = cache.get(theme, cache_key)
    if cached_result:
        return cached_result

    prompt = f"Generate a list of {n} well-known {theme}. Respond with only the names or titles, separated by commas."
    
    try:
        response = await client.chat.completions.create(
            model=config["model"],
            messages=[
                {"role": "system", "content": f"You are a helpful assistant generating lists of {theme}."},
                {"role": "user", "content": prompt}
            ]
        )
        entities = response.choices[0].message.content.strip().split(", ")
        result = entities[:n]
        cache.set(theme, cache_key, result)
        return result
    except Exception as e:
        logging.error(f"API call failed: {str(e)}")
        return []

async def compare_entities(entity1: str, entity2: str, theme: str, cache) -> str:
    cache_key = f"compare_{entity1}_{entity2}"
    cached_result = cache.get(theme, cache_key)
    if cached_result:
        return cached_result

    prompt = f"Compare {entity1} and {entity2} as {theme} in terms of 'Chad' qualities. Which one is more 'Chad' and why? A {theme} can be 'Chad' if it's influential, groundbreaking, or culturally significant. Respond with only the name or title of the winner."
    
    try:
        response = await client.chat.completions.create(
            model=config["model"],
            messages=[
                {"role": "system", "content": f"You are an AI assistant helping with a 'Virgin vs Chad' tournament of {theme}. Be humorous and slightly irreverent in your comparisons."},
                {"role": "user", "content": prompt}
            ]
        )
        winner = response.choices[0].message.content.strip()
        result = winner if winner in [entity1, entity2] else random.choice([entity1, entity2])
        cache.set(theme, cache_key, result)
        return result
    except Exception as e:
        logging.error(f"API call failed: {str(e)}")
        return random.choice([entity1, entity2])
