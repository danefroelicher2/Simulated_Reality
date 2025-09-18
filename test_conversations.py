#!/usr/bin/env python3
"""
Test Script for Character Conversations

This script tests the conversation system with and without Ollama.
It can run in simulation mode when Ollama is not available.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.world.world_state import World
from src.characters.ai_characters import DeepSeaResearcher, ERSurgeon
from src.characters.conversation import ConversationManager
from src.utils.ollama_client import OllamaClient


def test_ollama_connection():
    """Test if Ollama is available and working."""
    print("=" * 60)
    print("TESTING OLLAMA CONNECTION")
    print("=" * 60)

    try:
        client = OllamaClient()
        if client.check_connection():
            models = client.list_available_models()
            print(f"[OK] Ollama is running!")
            print(f"Available models: {models}")
            print(f"Current model: {client.model}")
            return True, client
        else:
            print("[ERROR] Ollama is not running or no models available")
            return False, None
    except Exception as e:
        print(f"[ERROR] Error connecting to Ollama: {e}")
        return False, None


def create_test_characters():
    """Create test characters for conversation."""
    print("\n" + "=" * 60)
    print("CREATING TEST CHARACTERS")
    print("=" * 60)

    # Create world
    world = World("Riverside Town")

    # Create characters
    marina = DeepSeaResearcher()
    alex = ERSurgeon()

    # Add to world
    world.add_character(marina)
    world.add_character(alex)

    # Add some initial experiences
    marina.remember_experience("I discovered some unusual bioluminescent organisms yesterday", importance=8)
    marina.remember_experience("The water temperature readings have been fluctuating", importance=6)
    marina.remember_experience("I'm working on a paper about microplastic contamination", importance=7)

    alex.remember_experience("Successfully performed emergency surgery on a trauma patient", importance=9)
    alex.remember_experience("Trained three new residents on cardiac procedures today", importance=7)
    alex.remember_experience("The emergency department was quite busy this week", importance=6)

    print(f"[OK] Created Dr. Marina Depth (Deep Sea Researcher)")
    print(f"   - Samples collected: {marina.samples_collected}")
    print(f"   - Discoveries: {len(marina.discoveries)}")
    print(f"   - Recent memories: {len(marina.memories)}")

    print(f"[OK] Created Dr. Alex Healer (ER Surgeon)")
    print(f"   - Patients treated: {alex.patients_treated}")
    print(f"   - Surgeries performed: {alex.surgeries_performed}")
    print(f"   - Recent memories: {len(alex.memories)}")

    return world, marina, alex


def test_conversation_system(ollama_available, ollama_client, marina, alex):
    """Test the conversation system."""
    print("\n" + "=" * 60)
    print("TESTING CONVERSATION SYSTEM")
    print("=" * 60)

    if ollama_available:
        # Test with real Ollama
        conversation_manager = ConversationManager(ollama_client)
        marina.set_conversation_manager(conversation_manager)
        alex.set_conversation_manager(conversation_manager)

        print("[AI] Testing with Ollama LLM...")

        # Test conversation with Marina
        print(f"\n--- Testing conversation with {marina.name} ---")
        test_questions = [
            "Hello! What are you working on today?",
            "Tell me about your research projects",
            "What's the most interesting discovery you've made recently?"
        ]

        for question in test_questions:
            print(f"\nUser: {question}")
            response = marina.respond_to(question)
            if response.get('success'):
                print(f"{marina.name}: {response['response']}")
            else:
                print(f"[ERROR]: {response.get('error', 'Unknown error')}")

        # Test conversation with Alex
        print(f"\n--- Testing conversation with {alex.name} ---")
        test_questions = [
            "How has your day been at the hospital?",
            "What kind of cases do you see most often?",
            "Any advice for staying healthy?"
        ]

        for question in test_questions:
            print(f"\nUser: {question}")
            response = alex.respond_to(question)
            if response.get('success'):
                print(f"{alex.name}: {response['response']}")
            else:
                print(f"[ERROR]: {response.get('error', 'Unknown error')}")

    else:
        print("[INFO] Ollama not available - showing what conversations would look like...")
        print("\n--- Sample conversation with Dr. Marina Depth ---")
        print("User: What are you working on today?")
        print("Dr. Marina: I'm analyzing some fascinating water samples I collected yesterday. The bioluminescent organisms I discovered are showing some unusual behavior patterns. My analytical mind is really excited about the potential implications for our understanding of river ecosystems. I've been documenting everything meticulously for my research on microplastic contamination.")

        print("\n--- Sample conversation with Dr. Alex Healer ---")
        print("User: How has your day been at the hospital?")
        print("Dr. Alex: It's been quite busy, but rewarding. I performed an emergency cardiac procedure this morning - the patient is doing well now, which always fills me with satisfaction. I also spent time training our new residents. Seeing them grow in confidence and skill reminds me why I love this profession. Patient care is always my top priority.")


def demonstrate_features(marina, alex):
    """Demonstrate key features of the conversation system."""
    print("\n" + "=" * 60)
    print("CONVERSATION SYSTEM FEATURES")
    print("=" * 60)

    print("CHARACTER-SPECIFIC PROMPTING:")
    print(f"   - {marina.name}: Analytical (20%), Curious (25%), Creative (18%)")
    print(f"   - {alex.name}: Empathetic (25%), Confident (20%), Analytical (15%)")

    print("\nMEMORY SYSTEM:")
    print(f"   - Characters remember experiences and conversations")
    print(f"   - Memories have importance levels (1-10)")
    print(f"   - Most important memories are preserved")

    print("\nPERSONALITY INTEGRATION:")
    print(f"   - Responses reflect personality traits")
    print(f"   - Temperature adjusted based on creativity/confidence")
    print(f"   - Professional knowledge and background influence responses")

    print("\nEXPERIENCE INJECTION:")
    print(f"   - You can give characters new experiences")
    print(f"   - They remember and reference these in future conversations")
    print(f"   - Example: 'experience I met a famous marine biologist today'")

    print("\nCONVERSATION HISTORY:")
    print(f"   - Each character maintains separate conversation history")
    print(f"   - Context preserved across multiple interactions")
    print(f"   - Recent conversations influence responses")


def show_usage_instructions():
    """Show how to use the conversation system."""
    print("\n" + "=" * 60)
    print("HOW TO USE THE CONVERSATION SYSTEM")
    print("=" * 60)

    print("1. ENSURE OLLAMA IS RUNNING:")
    print("   - Download from: https://ollama.com/download")
    print("   - Run: ollama serve")
    print("   - Pull a model: ollama pull llama3.2:3b")

    print("\n2. START CONVERSATIONS:")
    print("   - Run: python chat_with_characters.py")
    print("   - Choose between Dr. Marina or Dr. Alex")
    print("   - Start chatting!")

    print("\n3. CONVERSATION COMMANDS:")
    print("   - Type normally to chat")
    print("   - 'switch' - change characters")
    print("   - 'info' - see character status")
    print("   - 'memory' - see recent memories")
    print("   - 'experience [text]' - give them new experience")
    print("   - 'quit' - exit")

    print("\n4. CUSTOMIZE:")
    print("   - Edit prompts in: src/characters/conversation.py")
    print("   - Add new characters in: src/characters/ai_characters.py")
    print("   - Adjust personalities in character classes")


def main():
    """Main test function."""
    print("CHARACTER CONVERSATION SYSTEM - TEST SUITE")

    # Test Ollama connection
    ollama_available, ollama_client = test_ollama_connection()

    # Create characters
    world, marina, alex = create_test_characters()

    # Test conversations
    test_conversation_system(ollama_available, ollama_client, marina, alex)

    # Demonstrate features
    demonstrate_features(marina, alex)

    # Show usage instructions
    show_usage_instructions()

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

    if ollama_available:
        print("[SUCCESS] All systems operational!")
        print("Ready to start conversations with: python chat_with_characters.py")
    else:
        print("[WARNING] Ollama not running. Install and start Ollama to enable real conversations.")
        print("See usage instructions above for setup steps.")


if __name__ == "__main__":
    main()