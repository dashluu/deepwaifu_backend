# test_chat.py
import requests
import json
import uuid

# Server URL
BASE_URL = "http://localhost:8000"

# Create a new chat session
def create_chat():
    character = {
        "name": "Emma",
        "avatar": "avatar.jpg",
        "occupation": "Software Engineer",
        "personality": "friendly",
        "age": 28,
        "keywords": "tech, coding, coffee",
        "background": "Graduated from MIT, works at a tech startup",
        "interests": "hiking, reading sci-fi, playing guitar"
    }
    
    response = requests.post(f"{BASE_URL}/new-chat", json=character)
    return response.text.strip('"')  # Remove quotes from UUID

# Send a message
def send_message(ctx_id, message_text):
    message = {
        "ctx_id": ctx_id,
        "sender": "user",
        "receiver": "assistant",
        "content": message_text
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=message, stream=True)
    
    full_response = ""
    try:
        # Print status to debug
        print(f"Response status: {response.status_code}")
        
        for line in response.iter_lines(decode_unicode=True):
            if line:
                print(f"Received: {line}")
                # Check if it's SSE format (starts with "data: ")
                if line.startswith("data: "):
                    content = line[6:]  # Skip "data: " prefix
                    
                    # Check if this is the end marker
                    if content == "[DONE]":
                        break
                        
                    print(content, end='', flush=True)
                    full_response += content
                else:
                    # Handle non-SSE format
                    print(line, end='', flush=True)
                    full_response += line
    except Exception as e:
        print(f"\nError receiving response: {str(e)}")
    
    return full_response

# Run test
if __name__ == "__main__":
    ctx_id = create_chat()
    print(f"Created chat with ID: {ctx_id}")
    
    # Test messages
    test_messages = [
        "Hi, how are you today?",
        "Tell me about your background in technology",
        "What kind of projects do you work on?"
    ]
    
    for msg in test_messages:
        print(f"\nUser: {msg}")
        print("\nAssistant: ", end='')
        response = send_message(ctx_id, msg)
        print("\n" + "-"*50)