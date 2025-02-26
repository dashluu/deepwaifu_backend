from models import CharacterModel


class Context:
    def __init__(self, character: CharacterModel):
        self._character = character
        keywords = f"Defining traits: {character.keywords}." if character.keywords else ""
        background = f"Background: {character.background}." if character.background else ""
        interests = f"Interests: {character.interests}." if character.interests else ""
        self._role = f"""
            You are roleplaying as {character.name}, a {character.age}-year-old {character.occupation}.
            Personality: {character.personality}.
            {keywords}
            {background}
            {interests}
            Stay in character.
            Do not acknowledge being an AI or respond in ways that contradict your persona.
        """
        # Initial prompt that "tricks" the model into role-playing
        starter_prompt = {
            "role": "system",
            "content": self._role,
        }
        self._identity_prompt = {
            "role": "assistant",
            "content": self._role,
        }
        self._messages: list[dict[str, str]] = [starter_prompt]

    @property
    def character(self):
        return self._character

    @property
    def messages(self):
        return self._messages

    def add_message(self, message: dict[str, str]):
        self._messages.append(message)

    def inject_identity(self):
        self._messages.append(self._identity_prompt)

    def clear_all(self):
        # Clears everything except for the first prompt to trigger role-playing
        self._messages = self._messages[:1]
