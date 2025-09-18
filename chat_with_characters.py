#!/usr/bin/env python3
"""
Character Conversation Interface

Chat with Dr. Marina Depth (Deep Sea Researcher) and Dr. Alex Healer (ER Surgeon)
using Ollama-powered conversations that reflect their personalities and memories.
"""

import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.world.world_state import World
from src.characters.ai_characters import DeepSeaResearcher, ERSurgeon
from src.characters.conversation import ConversationManager
from src.utils.ollama_client import OllamaClient


class CharacterChatInterface:
    def __init__(self):
        self.world = None
        self.characters = {}
        self.conversation_manager = None
        self.current_character = None

    def initialize_system(self):
        """Initialize the world, characters, and conversation system."""
        print("=" * 60)
        print("    CHARACTER CONVERSATION INTERFACE")
        print("=" * 60)
        print("Initializing Riverside Town AI characters...")
        print()

        # Create world
        self.world = World("Riverside Town")

        # Create characters
        marina = DeepSeaResearcher()
        alex = ERSurgeon()

        # Add to world
        self.world.add_character(marina)
        self.world.add_character(alex)

        # Store characters
        self.characters = {
            "marina": marina,
            "alex": alex
        }

        # Initialize conversation system
        print("Setting up Ollama conversation system...")

        try:
            ollama_client = OllamaClient()

            # Test connection
            if not ollama_client.check_connection():
                print("[ERROR] Cannot connect to Ollama server.")
                print("Please make sure Ollama is running on localhost:11434")
                print("and you have a model available (e.g., llama3.2:3b)")
                return False

            self.conversation_manager = ConversationManager(ollama_client)

            # Set conversation managers for characters
            marina.set_conversation_manager(self.conversation_manager)
            alex.set_conversation_manager(self.conversation_manager)

            print(f"[OK] Connected to Ollama with model: {ollama_client.model}")
            print()

            # Give characters some initial experiences
            self._inject_initial_experiences()

            return True

        except Exception as e:
            print(f"[ERROR] Failed to initialize conversation system: {e}")
            return False

    def _inject_initial_experiences(self):
        """Give characters some initial memories to make conversations more interesting."""

        # Dr. Marina's experiences
        marina_experiences = [
            "I discovered an unusual bioluminescent algae strain in the river last week",
            "The water temperature readings have been fluctuating more than expected",
            "I'm particularly excited about my microplastic contamination research",
            "Yesterday I dove to 25 meters and collected some fascinating specimens",
            "I've been collaborating with marine biology colleagues via video conference"
        ]

        for exp in marina_experiences:
            self.characters["marina"].remember_experience(exp, importance=6)

        # Dr. Alex's experiences
        alex_experiences = [
            "I successfully performed an emergency cardiac procedure this morning",
            "Training the new residents on trauma care protocols has been rewarding",
            "The emergency supplies were running low, but I restocked everything",
            "I treated a patient with an unusual allergic reaction yesterday",
            "The community health outreach program is going very well"
        ]

        for exp in alex_experiences:
            self.characters["alex"].remember_experience(exp, importance=6)

        print("[INFO] Injected initial experiences into character memories")

    def show_character_info(self):
        """Display information about available characters."""
        print("AVAILABLE CHARACTERS:")
        print("-" * 40)

        marina = self.characters["marina"]
        alex = self.characters["alex"]

        print(f"1. Dr. Marina Depth (Deep Sea Researcher)")
        print(f"   Location: {marina.location}")
        print(f"   Mood: {marina.mood}, Energy: {marina.energy}%")
        print(f"   Top traits: {', '.join(marina.get_dominant_traits())}")
        print(f"   Samples collected: {marina.samples_collected}")
        print(f"   Discoveries: {len(marina.discoveries)}")
        print()

        print(f"2. Dr. Alex Healer (ER Surgeon)")
        print(f"   Location: {alex.location}")
        print(f"   Mood: {alex.mood}, Energy: {alex.energy}%")
        print(f"   Top traits: {', '.join(alex.get_dominant_traits())}")
        print(f"   Patients treated: {alex.patients_treated}")
        print(f"   Surgeries performed: {alex.surgeries_performed}")
        print()

    def select_character(self) -> bool:
        """Let user select which character to talk to."""
        while True:
            self.show_character_info()
            print("WHO WOULD YOU LIKE TO TALK TO?")
            print("1 - Dr. Marina Depth (Researcher)")
            print("2 - Dr. Alex Healer (Surgeon)")
            print("q - Quit")
            print()

            choice = input("Enter your choice (1/2/q): ").strip().lower()

            if choice == "q":
                return False
            elif choice == "1":
                self.current_character = self.characters["marina"]
                print(f"\n[CHAT] You are now talking to Dr. Marina Depth")
                print(f"She is currently at {self.current_character.location}")
                print("=" * 50)
                return True
            elif choice == "2":
                self.current_character = self.characters["alex"]
                print(f"\n[CHAT] You are now talking to Dr. Alex Healer")
                print(f"He is currently at {self.current_character.location}")
                print("=" * 50)
                return True
            else:
                print("Invalid choice. Please enter 1, 2, or q.")

    def chat_with_character(self):
        """Main chat loop with the selected character."""
        if not self.current_character:
            print("No character selected!")
            return

        character_name = self.current_character.name
        print(f"{character_name}: Hello! I'm ready to chat. What would you like to know?")
        print()
        print("CHAT COMMANDS:")
        print("- Type your message and press Enter to chat")
        print("- Type 'switch' to change characters")
        print("- Type 'info' to see character status")
        print("- Type 'memory' to see recent memories")
        print("- Type 'experience [text]' to give them a new experience")
        print("- Type 'quit' to exit")
        print("=" * 50)
        print()

        while True:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "quit":
                print(f"{character_name}: Goodbye! It was nice talking with you.")
                break
            elif user_input.lower() == "switch":
                print(f"{character_name}: I'll talk to you later!")
                return "switch"
            elif user_input.lower() == "info":
                self._show_character_status()
                continue
            elif user_input.lower() == "memory":
                self._show_character_memories()
                continue
            elif user_input.lower().startswith("experience "):
                experience = user_input[11:]  # Remove "experience " prefix
                self.current_character.remember_experience(experience, importance=7)
                print(f"[SYSTEM] Gave {character_name} the experience: {experience}")
                continue

            # Generate response
            print(f"{character_name}: ", end="", flush=True)

            try:
                response_data = self.current_character.respond_to(user_input)

                if response_data.get('success', False):
                    print(response_data['response'])
                else:
                    print(f"[Error: {response_data.get('error', 'Unknown error')}]")

            except Exception as e:
                print(f"[System Error: {e}]")

            print()

        return "quit"

    def _show_character_status(self):
        """Show current character status."""
        char = self.current_character
        print(f"\n[INFO] {char.name} Status:")
        print(f"  Location: {char.location}")
        print(f"  Activity: {char.current_activity}")
        print(f"  Mood: {char.mood}")
        print(f"  Energy: {char.energy}%")

        if hasattr(char, 'samples_collected'):
            print(f"  Samples collected: {char.samples_collected}")
            print(f"  Discoveries: {len(char.discoveries)}")
        elif hasattr(char, 'patients_treated'):
            print(f"  Patients treated: {char.patients_treated}")
            print(f"  Surgeries performed: {char.surgeries_performed}")

        print(f"  Relationships: {len(char.relationships)}")
        print()

    def _show_character_memories(self):
        """Show character's recent memories."""
        char = self.current_character
        if hasattr(char, 'memories') and char.memories:
            print(f"\n[MEMORIES] {char.name}'s recent memories:")
            for i, memory in enumerate(char.memories[-5:], 1):
                print(f"  {i}. {memory['content']} (importance: {memory['importance']})")
        else:
            print(f"\n[MEMORIES] {char.name} has no recent memories.")
        print()

    def run(self):
        """Main application loop."""
        if not self.initialize_system():
            return

        print("Conversation system ready!")
        print()

        while True:
            if not self.select_character():
                print("Goodbye!")
                break

            result = self.chat_with_character()
            if result == "quit":
                print("Goodbye!")
                break


def main():
    """Entry point for the character chat interface."""
    try:
        chat_interface = CharacterChatInterface()
        chat_interface.run()
    except KeyboardInterrupt:
        print("\n\n[STOP] Chat interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()