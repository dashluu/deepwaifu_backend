from context import Context
from models import MessageModel
import asyncio
from ollama import chat


class CharacterEngine:
    def __init__(self, model="llama3"):
        self._model = model

    async def generate_response(self, ctx: Context, message: MessageModel):
        ctx.add_message({"role": "user", "content": message.text})
        # Check history
        # print(messages)
        if len(ctx.messages) % 5 == 0:
            ctx.inject_identity()
        response = chat(model=self._model, messages=ctx.messages, stream=True)
        ctx.add_message({"role": "assistant", "content": ""})
        for chunk in response:
            ctx.messages[-1]["content"] += chunk["message"]["content"]
            yield chunk["message"]["content"]
            # Force flush the chunk
            await asyncio.sleep(0)
