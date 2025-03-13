from models import CharacterModel # represent a character -> from models.py

# manages roleplaying chatbot -> makes sure AI stays in character
# character : character you have selected
class Context:
    def __init__(self, character):
        self.character = character
        self.messages = []
        
    def add_message(self, message):
        self.messages.append(message)
        
    def clear_all(self):
        self.messages = []
        
    def inject_identity(self):
        """Injects character identity into the conversation to reinforce persona"""
        identity_prompt = {
            "role": "system", 
            "content": f"You are {self.character.name}, a {self.character.age}-year-old {self.character.occupation} with a {self.character.personality} personality. " +
                       f"Background: {self.character.background}. " +
                       f"Interests: {self.character.interests}."
        }
        # Insert at the beginning of the messages list
        self.messages.insert(0, identity_prompt)
