from models import ContextModel
from context import Context


class ContextManagerError(Exception):
    def __init__(self):
        super().__init__("Invalid chat context.")


class ContextManager:
    def __init__(self):
        self._ctxs: dict[str, Context] = {}

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
        self._ctxs[ctx.id] = Context(character, starter)

    def get_context(self, id: str) -> Context:
        if id not in self._ctxs:
            raise ContextManagerError()
        return self._ctxs[id]

    def delete_context(self, id: str):
        if id not in self._ctxs:
            raise ContextManagerError()
        del self._ctxs[id]

    def __str__(self):
        return str(self._ctxs)
