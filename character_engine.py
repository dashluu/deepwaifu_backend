from context import Context # convo history -> from context.py
from models import MessageModel # message from user -> from models.py
import asyncio # asynch operations
from ollama import chat # llama3 model


class CharacterEngine:
    def __init__(self, model="llama3"):
        self._model = model

    # Asynchronous generator
    async def generate_response(self, ctx: Context, message: MessageModel):
        ctx.add_message({"role": "user", "content": message.text}) # add user's message to convo history

        # if len(ctx.messages) % 5 == 0: # every 5 messages, injects identity (to reinforce persona)
        #     ctx.inject_identity()
        
        response = chat(model=self._model, messages=ctx.messages, stream=True) # calls model w/ history
        ctx.add_message({"role": "assistant", "content": ""}) # placeholder for ai response
        
        for chunk in response:
            ctx.messages[-1]["content"] += chunk["message"]["content"] # basically just adding word one at a time --> (I) -> (I am) -> (I am a) -> (I am a llama)
            yield chunk["message"]["content"] # progressive appearance
            # Force flush the chunk
            await asyncio.sleep(0)

        # example:
        # ctx.messages = [] for initial state
        # the user says hello --> ctx.add_message({"role": "user", "content": "Hello"})
        # now ctx.messages = [ {"role": "user", "content": "Hello"} ]
        # model says "how are you?" --> ctx.add_message({"role": "assistant", "content": "how are you?"})
        # now ctx.messages = [ {"role": "user", "content": "Hello"}, {"role": "assistant", "content": "how are you?"} ]        
