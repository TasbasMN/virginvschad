import random
import asyncio
import keyring
from openai import AsyncOpenAI

def get_openai_api_key():
    return keyring.get_password("system", "openai_api_key")

client = AsyncOpenAI(api_key=get_openai_api_key())

async def generate_entities(n, theme):
    prompt = f"Generate a list of {n} well-known {theme}. Respond with only the names or titles, separated by commas."
    
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant generating lists of {theme}."},
                {"role": "user", "content": prompt}
            ]
        )
        entities = response.choices[0].message.content.strip().split(", ")
        return entities[:n]
    except Exception as e:
        print(f"API call failed: {str(e)}")
        return []

async def compare_entities(entity1, entity2, theme):
    prompt = f"Compare {entity1} and {entity2} as {theme} in terms of 'Chad' qualities. Which one is more 'Chad' and why? A {theme} can be 'Chad' if it's influential, groundbreaking, or culturally significant. Respond with only the name or title of the winner."
    
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are an AI assistant helping with a 'Virgin vs Chad' tournament of {theme}. Be humorous and slightly irreverent in your comparisons."},
                {"role": "user", "content": prompt}
            ]
        )
        winner = response.choices[0].message.content.strip()
        return winner if winner in [entity1, entity2] else random.choice([entity1, entity2])
    except Exception as e:
        print(f"API call failed: {str(e)}")
        return random.choice([entity1, entity2])

async def tournament(entities, theme):
    rounds = 1
    
    while len(entities) > 1:
        print(f"\nRound {rounds}:")
        winners = []
        for i in range(0, len(entities), 2):
            if i + 1 < len(entities):
                entity1, entity2 = entities[i], entities[i+1]
                winner = await compare_entities(entity1, entity2, theme)
                print(f"{entity1} vs {entity2} - Chad: {winner}")
                winners.append(winner)
            else:
                print(f"{entities[i]} advances automatically (Chad by default)")
                winners.append(entities[i])
        
        entities = winners
        rounds += 1
    
    return entities[0]

async def main():
    n = int(input("Enter the number of entities for the Chad tournament: "))
    theme = input("Enter a theme (e.g., 'books', 'movies', 'historical figures'): ").strip()
    
    entities = await generate_entities(n, theme)
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