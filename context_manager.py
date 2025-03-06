from models import ContextModel # represents chat session -> from models.py
from context import Context # convo history -> from context.py


class ContextManagerError(Exception):
    def __init__(self):
        super().__init__("Invalid chat context.")

# Class allows for multiple chat contexts
# Main reason to use is to create a persona for each new character
class ContextManager:
    def __init__(self):
        self._ctxs: dict[str, Context] = {} # context ids, Context object

    # Creates a new context object
    # ctx: object ctx which is an ID, character
    def add_context(self, ctx: ContextModel):
        self._ctxs[ctx.id] = Context(ctx.character) # adds new context to dict

    # Given an id, retrieves corresponding context
    # id: specific context id
    def get_context(self, id: str) -> Context:
        if id not in self._ctxs:
            raise ContextManagerError()
        return self._ctxs[id]

    # Given an id, deletes corresponding context
    # id: specific context id
    def delete_context(self, id: str):
        if id not in self._ctxs:
            raise ContextManagerError()
        del self._ctxs[id]

    # converts dictionary of contexts to string
    def __str__(self):
        return str(self._ctxs)
