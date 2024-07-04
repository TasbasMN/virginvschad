import random
import asyncio
from pathlib import Path
from typing import List
from .cache import FileCache
from .openai_client import generate_entities, compare_entities

# Initialize cache
cache = FileCache(Path("data/chad_cache.json"))

async def tournament(entities: List[str], theme: str) -> str:
    rounds = 1
    
    while len(entities) > 1:
        print(f"\nRound {rounds}:")
        winners = []
        comparisons = []
        for i in range(0, len(entities), 2):
            if i + 1 < len(entities):
                entity1, entity2 = entities[i], entities[i+1]
                comparisons.append(compare_entities(entity1, entity2, theme, cache))
            else:
                print(f"{entities[i]} advances automatically (Chad by default)")
                winners.append(entities[i])
        
        results = await asyncio.gather(*comparisons)
        winners.extend(results)
        
        for i, winner in enumerate(results):
            print(f"{entities[i*2]} vs {entities[i*2+1]} - Chad: {winner}")
        
        entities = winners
        rounds += 1
    
    return entities[0]

async def main():
    try:
        n = int(input("Enter the number of entities for the Chad tournament: "))
        if n <= 1:
            raise ValueError("Number of entities must be greater than 1")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    theme = input("Enter a theme (e.g., 'books', 'movies', 'historical figures'): ").strip()
    if not theme:
        print("Theme cannot be empty")
        return
    
    entities = await generate_entities(n, theme, cache)
    if not entities:
        print("Failed to generate entities. Exiting.")
        return
    
    print(f"Generated list of potentially Chad {theme}:")
    print(", ".join(entities))
    
    random.shuffle(entities)
    
    final_chad = await tournament(entities, theme)
    print(f"\nThe Ultimate Chad {theme.capitalize()} is: {final_chad}")

if __name__ == "__main__":
    asyncio.run(main())
