import random
import asyncio
import keyring
from openai import AsyncOpenAI
from typing import List, Optional
import logging
import json
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config_path = Path("config.json")
with config_path.open() as f:
    config = json.load(f)

def get_openai_api_key() -> str:
    return keyring.get_password("system", "openai_api_key")

client = AsyncOpenAI(api_key=get_openai_api_key())

# Simple in-memory cache
cache = {}

async def generate_entities(n: int, theme: str) -> List[str]:
    cache_key = f"generate_{n}_{theme}"
    if cache_key in cache:
        return cache[cache_key]

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
        cache[cache_key] = result
        return result
    except Exception as e:
        logging.error(f"API call failed: {str(e)}")
        return []

async def compare_entities(entity1: str, entity2: str, theme: str) -> str:
    cache_key = f"compare_{entity1}_{entity2}_{theme}"
    if cache_key in cache:
        return cache[cache_key]

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
        cache[cache_key] = result
        return result
    except Exception as e:
        logging.error(f"API call failed: {str(e)}")
        return random.choice([entity1, entity2])

async def tournament(entities: List[str], theme: str) -> str:
    rounds = 1
    
    while len(entities) > 1:
        logging.info(f"\nRound {rounds}:")
        winners = []
        comparisons = []
        for i in range(0, len(entities), 2):
            if i + 1 < len(entities):
                entity1, entity2 = entities[i], entities[i+1]
                comparisons.append(compare_entities(entity1, entity2, theme))
            else:
                logging.info(f"{entities[i]} advances automatically (Chad by default)")
                winners.append(entities[i])
        
        results = await asyncio.gather(*comparisons)
        winners.extend(results)
        
        for i, winner in enumerate(results):
            logging.info(f"{entities[i*2]} vs {entities[i*2+1]} - Chad: {winner}")
        
        entities = winners
        rounds += 1
    
    return entities[0]

async def main():
    try:
        n = int(input("Enter the number of entities for the Chad tournament: "))
        if n <= 1:
            raise ValueError("Number of entities must be greater than 1")
    except ValueError as e:
        logging.error(f"Invalid input: {e}")
        return

    theme = input("Enter a theme (e.g., 'books', 'movies', 'historical figures'): ").strip()
    if not theme:
        logging.error("Theme cannot be empty")
        return
    
    entities = await generate_entities(n, theme)
    if not entities:
        logging.error("Failed to generate entities. Exiting.")
        return
    
    logging.info(f"Generated list of potentially Chad {theme}:")
    logging.info(", ".join(entities))
    
    random.shuffle(entities)
    
    final_chad = await tournament(entities, theme)
    logging.info(f"\nThe Ultimate Chad {theme.capitalize()} is: {final_chad}")

if __name__ == "__main__":
    asyncio.run(main())
