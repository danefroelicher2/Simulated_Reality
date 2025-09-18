#!/usr/bin/env python3
"""
Conversation System Demo

Demonstrates how the Ollama conversation integration works with character personalities,
memories, and experiences. This script shows the system without requiring Ollama to be running.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.world.world_state import World
from src.characters.ai_characters import DeepSeaResearcher, ERSurgeon
from src.characters.conversation import ConversationManager


class MockOllamaClient:
    """Mock Ollama client for demonstration purposes."""

    def __init__(self):
        self.model = "llama3.2:3b (simulated)"
        self.conversation_history = {}

    def check_connection(self):
        return True

    def generate_response(self, prompt, character_id, system_prompt, temperature=0.7, max_tokens=400):
        """Generate a mock response based on character type."""

        # Simple mock responses based on character and prompt content
        if "Deep_Sea_Researcher" in character_id:
            if "research" in prompt.lower() or "discovery" in prompt.lower():
                response = "I'm incredibly excited about my current research! The river ecosystem here is fascinating, and I've been collecting samples that show some unusual bioluminescent properties. My analytical nature drives me to understand every detail of these phenomena."
            elif "hello" in prompt.lower() or "hi" in prompt.lower():
                response = "Hello! I'm Dr. Marina Depth. I'm always curious to learn about new perspectives. What brings you to our research station today? Are you interested in marine biology or perhaps the unique ecosystem of our river?"
            elif "personality" in prompt.lower() or "traits" in prompt.lower():
                response = "My personality is strongly driven by curiosity - it's what led me to deep sea research in the first place. I'm very analytical in my approach, always seeking to understand the 'why' behind natural phenomena. I also have a creative side that helps me develop innovative research methods."
            else:
                response = "That's an interesting question! My research background has taught me to approach problems systematically. I'd love to dive deeper into this topic - curiosity is one of my strongest traits, after all."

        elif "ER_Surgeon" in character_id:
            if "patient" in prompt.lower() or "medical" in prompt.lower():
                response = "Patient care is my absolute priority. Every person who comes through our emergency department deserves compassionate, expert treatment. My 15 years of experience have taught me that empathy and medical skill must work hand in hand."
            elif "hello" in prompt.lower() or "hi" in prompt.lower():
                response = "Hello! I'm Dr. Alex Healer, the ER surgeon here at Riverside General Hospital. How are you feeling today? Is there anything I can help you with? I always like to check on people's wellbeing - it's just part of who I am."
            elif "personality" in prompt.lower() or "traits" in prompt.lower():
                response = "Empathy drives everything I do in medicine. I also have the confidence needed to make critical decisions under pressure - that's essential in emergency surgery. My analytical thinking helps me diagnose complex cases accurately."
            else:
                response = "That's something I approach with both confidence and empathy. In my medical practice, I've learned that every situation requires careful consideration of both the technical and human elements involved."

        else:
            response = "I'm not sure how to respond to that right now."

        return {
            "response": response,
            "success": True,
            "timestamp": "2025-09-17T21:30:00",
            "character_id": character_id,
            "model": self.model,
            "tokens_used": len(response.split()),
            "metadata": {
                "temperature": temperature,
                "max_tokens": max_tokens,
                "prompt_length": len(prompt)
            }
        }

    def clear_conversation_history(self, character_id=None):
        if character_id:
            if character_id in self.conversation_history:
                del self.conversation_history[character_id]
        else:
            self.conversation_history.clear()

    def get_conversation_summary(self, character_id):
        return {"message_count": 0, "history": []}

    def list_available_models(self):
        return ["llama3.2:3b (simulated)", "llama3.1:8b (simulated)"]

    def switch_model(self, model_name):
        self.model = model_name
        return True


def demonstrate_conversation_system():
    """Demonstrate the conversation system with mock responses."""

    print("=" * 60)
    print("    CONVERSATION SYSTEM DEMONSTRATION")
    print("=" * 60)
    print("This demo shows how AI characters respond with their personalities")
    print("using the Ollama integration system (with simulated responses).")
    print()

    # Initialize world and characters
    world = World("Riverside Town")
    marina = DeepSeaResearcher()
    alex = ERSurgeon()

    world.add_character(marina)
    world.add_character(alex)

    # Set up conversation system with mock client
    mock_client = MockOllamaClient()
    conversation_manager = ConversationManager(mock_client)

    # Connect conversation managers
    marina.set_conversation_manager(conversation_manager)
    alex.set_conversation_manager(conversation_manager)

    print("[DEMO] Characters created and conversation system initialized")
    print(f"Model: {mock_client.model}")
    print()

    # Give characters some experiences to reference
    marina.remember_experience("I discovered unusual algae in the river yesterday", importance=8)
    marina.remember_experience("The water temperature readings are fluctuating", importance=6)
    alex.remember_experience("I performed emergency surgery on a trauma patient", importance=8)
    alex.remember_experience("Training new residents has been very rewarding", importance=5)

    print("[DEMO] Injected experiences into character memories")
    print()

    # Demonstrate conversations
    test_conversations = [
        ("Hello Dr. Marina, tell me about yourself", "marina"),
        ("What kind of research are you working on?", "marina"),
        ("How does your personality influence your work?", "marina"),
        ("Hello Dr. Alex, how are you doing?", "alex"),
        ("Tell me about your medical practice", "alex"),
        ("What personality traits help you as a surgeon?", "alex")
    ]

    for question, character_key in test_conversations:
        character = marina if character_key == "marina" else alex

        print(f"[USER] {question}")
        print(f"[{character.name}] ", end="")

        try:
            response_data = character.respond_to(question)

            if response_data.get('success', False):
                print(response_data['response'])
                print(f"[METADATA] Temperature: {response_data['metadata']['temperature']:.2f}, "
                      f"Tokens: {response_data['tokens_used']}")
            else:
                print(f"[Error: {response_data.get('error', 'Unknown error')}]")

        except Exception as e:
            print(f"[System Error: {e}]")

        print("-" * 60)
        print()

    # Show character memories
    print("[DEMO] Character Memories After Conversations:")
    print()

    for char_name, char in [("Dr. Marina", marina), ("Dr. Alex", alex)]:
        print(f"{char_name}'s Recent Memories:")
        if hasattr(char, 'memories') and char.memories:
            for i, memory in enumerate(char.memories[-3:], 1):
                print(f"  {i}. {memory['content']} (importance: {memory['importance']})")
        print()

    # Show system capabilities
    print("[SYSTEM] Conversation System Capabilities:")
    print("+ Character-specific personality prompting")
    print("+ Memory formation from conversations")
    print("+ Experience injection system")
    print("+ Personality trait integration")
    print("+ Professional context awareness")
    print("+ Conversation history tracking")
    print("+ Dynamic temperature adjustment based on personality")
    print()

    print("[INFO] To use with real Ollama:")
    print("1. Install Ollama: https://ollama.com/download")
    print("2. Run: ollama pull llama3.2:3b")
    print("3. Start Ollama server")
    print("4. Run: python chat_with_characters.py")
    print()

    print("Ready for real AI conversations!")


if __name__ == "__main__":
    demonstrate_conversation_system()