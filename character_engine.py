from context import Context
from models import MessageModel
import asyncio
from ollama import chat


class CharacterEngine:
    def __init__(self, model="llama3"):
        self._model = model

    async def generate_response(self, ctx: Context, message: MessageModel):
        ctx.messages.append({"role": "user", "content": message.text})
        # Check history
        # print(messages)
        identity_prompt = {
            "role": "system",
            "content": f"""
                You are roleplaying as {ctx.character.name}, a {ctx.character.age}-year-old {ctx.character.occupation}.
                Your personality is: {ctx.character.personality}.
                Your defining traits include: {ctx.character.keywords}.
                Stay in character.
                Do not acknowledge being an AI or respond in ways that contradict your persona.
            """
        }
        if len(ctx.messages) % 5 == 0:
            ctx.messages.append(identity_prompt)

        response = chat(model=self._model, messages=ctx.messages, stream=True)
        ctx.messages.append({"role": "assistant", "content": ""})
        
        for chunk in response:
            ctx.messages[-1]["content"] += chunk["message"]["content"]
            yield chunk["message"]["content"]
            # Force flush the chunk
            await asyncio.sleep(0)