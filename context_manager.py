from models import MessageModel, ContextModel, CharacterModel
import asyncio
from ollama import chat


class ContextManager:
    def __init__(self, model="llama3"):
        self._ctxs: dict[str, tuple[CharacterModel, list[dict[str, str]]]] = {}
        self._model = model

    def add_context(self, ctx: ContextModel):
        character = ctx.character
        # Initial prompt that "tricks" the model into role-playing
        starter = {
            "role": "system",
            "content": f"""
                This is a role playing.
                Your name is {character.name}.
                You are {character.age}.
                Your occupation is {character.occupation}.
                Your personality is {character.personality}.
                Your keywords are {character.keywords}.
            """,
        }
        self._ctxs[ctx.id] = (character, [starter])

    def clear_context(self, ctx_id: str):
        # Clears everything except for the first prompt to trigger role-playing
        if ctx_id not in self._ctxs:
            raise Exception("Invalid conversation.")
        ctx = self._ctxs[ctx_id]
        ctx[1] = [ctx[1][0]]

    # Gets the character associated with a context ID, or conversation ID
    def get_character(self, ctx_id: str):
        if ctx_id not in self._ctxs:
            raise Exception("Invalid conversation.")
        return self._ctxs[ctx_id][0]

    async def generate_response(self, message: MessageModel):
        messages = self._ctxs[message.ctx_id][1]
        messages.append({"role": "user", "content": message.text})
        # Check history
        # print(messages)
        response = chat(model=self._model, messages=messages, stream=True)
        messages.append({"role": "assistant", "content": ""})
        for chunk in response:
            messages[-1]["content"] += chunk["message"]["content"]
            yield chunk["message"]["content"]
            # Force flush the chunk
            await asyncio.sleep(0)
