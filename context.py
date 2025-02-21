from models import CharacterModel


class Context:
    def __init__(self, character: CharacterModel, starter: dict[str, str]):
        self._character = character
        self._messages: list[dict[str, str]] = [starter]

    @property
    def character(self):
        return self._character

    @property
    def messages(self):
        return self._messages

    def add_message(self, message: dict[str, str]):
        self._messages.append(message)

    def clear_all(self):
        # Clears everything except for the first prompt to trigger role-playing
        self._messages = self._messages[:1]
