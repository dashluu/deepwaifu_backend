from context import Context # convo history
from models import MessageModel # message from user
import asyncio # asynch operations
from ollama import chat # llama3 model


class CharacterEngine:
    # Initialize the model (default = llama3)
    def __init__(self, model="llama3"):
        self._model = model

    # Asynchronous generator
    async def generate_response(self, ctx: Context, message: MessageModel):
        ctx.add_message({"role": "user", "content": message.text}) # add user's message to convo history
        # Check history
        # print(messages)

        if len(ctx.messages) % 5 == 0: # every 5 messages, injects identity (to reinforce persona)
            ctx.inject_identity()
        response = chat(model=self._model, messages=ctx.messages, stream=True) # calls model w/ history
        ctx.add_message({"role": "assistant", "content": ""}) # placeholder for ai response
        for chunk in response:
            ctx.messages[-1]["content"] += chunk["message"]["content"]
            yield chunk["message"]["content"]
            # Force flush the chunk
            await asyncio.sleep(0)
