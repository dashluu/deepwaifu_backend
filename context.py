from models import CharacterModel # represent a character -> from models.py

# manages roleplaying chatbot -> makes sure AI stays in character
# character : character you have selected
class Context:
    def __init__(self, character: CharacterModel):
        self._character = character # basic character information (name, age, etc.)
        # description of character
        keywords = f"Defining traits: {character.keywords}." if character.keywords else ""
        background = f"Background: {character.background}." if character.background else ""
        interests = f"Interests: {character.interests}." if character.interests else ""

        # Roleplaying prompt
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

        # stores conversation history
        self._messages: list[dict[str, str]] = [starter_prompt]

    # returns characterModel instance
    @property
    def character(self):
        return self._character

    # returns list of chat messages
    @property
    def messages(self):
        return self._messages

    # adds message to chat history
    def add_message(self, message: dict[str, str]):
        self._messages.append(message)

    # injects identity prompt (not needed anymore)
    def inject_identity(self):
        self._messages.append(self._identity_prompt)

    # clears chat history
    def clear_all(self):
        # Clears everything except for the first prompt to trigger role-playing
        self._messages = self._messages[:1]
