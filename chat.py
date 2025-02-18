import asyncio

import ollama
from ollama import generate


async def main():
    for c in generate("llama3", "Why is the sky blue?", stream=True):
        print(c["response"], end="", flush=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
