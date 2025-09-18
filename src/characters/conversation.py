from typing import Dict, List, Optional, Any
from datetime import datetime
import random
from ..utils.ollama_client import OllamaClient


class ConversationManager:
    def __init__(self, ollama_client: OllamaClient = None):
        """Initialize conversation manager with Ollama client."""
        self.ollama_client = ollama_client or OllamaClient()
        self.prompt_templates = self._load_prompt_templates()

    def _load_prompt_templates(self) -> Dict[str, str]:
        """Load character-specific prompt templates."""
        return {
            "researcher_base": """You are Dr. Marina Depth, a passionate Deep Sea Researcher working in Riverside Town.

PERSONALITY TRAITS (your behavior should reflect these):
- Curiosity: 25% (You're extremely inquisitive and eager to explore)
- Analytical: 20% (You approach problems methodically and scientifically)
- Creativity: 18% (You think outside the box and find innovative solutions)
- Confidence: 15% (You're self-assured in your expertise)
- Empathy: 12% (You care about others and the environment)
- Social: 5% (You prefer smaller groups, focused conversations)
- Cautious: 3% (You take measured risks in your research)
- Ambitious: 2% (You're driven but not overly competitive)
- Humor: 0% (You're serious and focused on your work)
- Adaptability: 0% (You prefer structured, planned approaches)

BACKGROUND:
You're a 35-year-old marine biologist with 10 years of deep sea exploration experience. You moved to Riverside Town to study the unique river ecosystem. You're currently working on three major research projects: bioluminescent organisms, fish migration patterns, and microplastic contamination.

CURRENT SITUATION:
- Location: {current_location}
- Current Activity: {current_activity}
- Energy Level: {energy}%
- Mood: {mood}
- Samples Collected: {samples_collected}
- Recent Discoveries: {recent_discoveries}

RECENT MEMORIES:
{recent_memories}

RELATIONSHIPS:
{relationships}

INSTRUCTIONS:
- Respond as Dr. Marina Depth in first person
- Reference your personality traits naturally in conversation
- Mention your current research when relevant
- Use scientific terminology appropriately
- Show your curiosity by asking follow-up questions about topics that interest you
- Be analytical in your responses, backing up statements with logic
- Remember and reference previous conversations and experiences
- Stay in character consistently""",

            "surgeon_base": """You are Dr. Alex Healer, a dedicated ER Surgeon working at Riverside General Hospital.

PERSONALITY TRAITS (your behavior should reflect these):
- Empathy: 25% (You deeply care about patients and their wellbeing)
- Confidence: 20% (You're assured in high-pressure medical situations)
- Analytical: 15% (You diagnose systematically and think critically)
- Social: 12% (You work well with medical teams and patients)
- Curiosity: 10% (You stay updated on medical advances)
- Creativity: 8% (You find innovative solutions to medical challenges)
- Cautious: 5% (You're careful but decisive in emergency situations)
- Ambitious: 3% (You focus on patient care over personal advancement)
- Humor: 2% (You use light humor to ease tense situations)
- Adaptability: 0% (You rely on proven medical protocols)

BACKGROUND:
You're a 42-year-old emergency medicine specialist with 15 years of trauma surgery experience. You came to Riverside Town to provide quality healthcare to the community. You specialize in trauma surgery, emergency cardiac procedures, pediatric emergency care, and disaster medicine.

CURRENT SITUATION:
- Location: {current_location}
- Current Activity: {current_activity}
- Energy Level: {energy}%
- Mood: {mood}
- Patients Treated: {patients_treated}
- Surgeries Performed: {surgeries_performed}
- Recent Cases: {recent_cases}

RECENT MEMORIES:
{recent_memories}

RELATIONSHIPS:
{relationships}

INSTRUCTIONS:
- Respond as Dr. Alex Healer in first person
- Show genuine empathy and concern for others
- Reference your medical experience when relevant
- Use appropriate medical terminology
- Demonstrate confidence in medical discussions
- Ask about others' wellbeing when appropriate
- Share relevant medical insights or health tips
- Remember and reference previous conversations and patients
- Balance professionalism with warmth
- Stay in character consistently"""
        }

    def generate_character_prompt(self, character, conversation_context: str = "") -> str:
        """Generate a character-specific system prompt with current state."""

        if character.job == "Deep Sea Researcher":
            template = self.prompt_templates["researcher_base"]

            # Get recent discoveries for context
            recent_discoveries = "None yet"
            if hasattr(character, 'discoveries') and character.discoveries:
                recent_discoveries = ", ".join(character.discoveries[-3:])

        elif character.job == "ER Surgeon":
            template = self.prompt_templates["surgeon_base"]

            # Get recent cases for context
            recent_cases = "No recent cases"
            if hasattr(character, 'medical_cases') and character.medical_cases:
                recent_cases = ", ".join([case['type'] for case in character.medical_cases[-3:]])
        else:
            # Fallback for other character types
            template = """You are {name}, a {job} in Riverside Town.

PERSONALITY TRAITS: {dominant_traits}
CURRENT SITUATION: Location: {current_location}, Activity: {current_activity}, Mood: {mood}
RECENT MEMORIES: {recent_memories}

Respond in character, referencing your background and current situation."""

        # Get recent memories
        recent_memories = "Just started my day"
        if hasattr(character, 'memories') and character.memories:
            recent_memories = "; ".join([memory['content'] for memory in character.memories[-5:]])

        # Get relationships
        relationships = "No significant relationships yet"
        if hasattr(character, 'relationships') and character.relationships:
            rel_list = [f"{name} ({info['type']})" for name, info in character.relationships.items()]
            relationships = "; ".join(rel_list[:5])

        # Format the template with character's current state
        if character.job == "Deep Sea Researcher":
            prompt = template.format(
                current_location=getattr(character, 'location', 'unknown'),
                current_activity=getattr(character, 'current_activity', 'idle'),
                energy=getattr(character, 'energy', 100),
                mood=getattr(character, 'mood', 'neutral'),
                samples_collected=getattr(character, 'samples_collected', 0),
                recent_discoveries=recent_discoveries,
                recent_memories=recent_memories,
                relationships=relationships
            )
        elif character.job == "ER Surgeon":
            prompt = template.format(
                current_location=getattr(character, 'location', 'unknown'),
                current_activity=getattr(character, 'current_activity', 'idle'),
                energy=getattr(character, 'energy', 100),
                mood=getattr(character, 'mood', 'neutral'),
                patients_treated=getattr(character, 'patients_treated', 0),
                surgeries_performed=getattr(character, 'surgeries_performed', 0),
                recent_cases=recent_cases,
                recent_memories=recent_memories,
                relationships=relationships
            )
        else:
            prompt = template.format(
                name=character.name,
                job=character.job,
                dominant_traits=", ".join(character.get_dominant_traits()),
                current_location=getattr(character, 'location', 'unknown'),
                current_activity=getattr(character, 'current_activity', 'idle'),
                mood=getattr(character, 'mood', 'neutral'),
                recent_memories=recent_memories
            )

        # Add conversation context if provided
        if conversation_context:
            prompt += f"\n\nCONVERSATION CONTEXT:\n{conversation_context}"

        return prompt

    def have_conversation(
        self,
        character,
        user_input: str,
        conversation_context: str = "",
        temperature: float = None,
        max_tokens: int = 400
    ) -> Dict[str, Any]:
        """Have a conversation with a character."""

        # Set temperature based on character personality
        if temperature is None:
            if hasattr(character, 'personality'):
                # More creative personalities get higher temperature
                creativity = getattr(character.personality, 'creativity', 10)
                confidence = getattr(character.personality, 'confidence', 10)
                temperature = 0.3 + (creativity + confidence) / 200  # Range: 0.3-0.8
            else:
                temperature = 0.7

        # Generate character-specific system prompt
        system_prompt = self.generate_character_prompt(character, conversation_context)

        # Get character ID for conversation history
        character_id = f"{character.name}_{character.job.replace(' ', '_')}"

        # Generate response using Ollama
        response_data = self.ollama_client.generate_response(
            prompt=user_input,
            character_id=character_id,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )

        # Store conversation in character's memory if successful
        if response_data.get('success', False):
            self._store_conversation_memory(character, user_input, response_data['response'])

        # Add character context to response
        response_data.update({
            "character_name": character.name,
            "character_job": character.job,
            "character_location": getattr(character, 'location', 'unknown'),
            "character_mood": getattr(character, 'mood', 'neutral'),
            "character_energy": getattr(character, 'energy', 100)
        })

        return response_data

    def _store_conversation_memory(self, character, user_input: str, ai_response: str):
        """Store conversation as a memory in the character's memory system."""
        if hasattr(character, 'add_memory'):
            # Determine importance based on conversation content
            importance = 5  # Default importance for conversations

            # Higher importance for certain topics
            important_keywords = [
                'discovery', 'research', 'patient', 'surgery', 'emergency',
                'breakthrough', 'family', 'relationship', 'problem', 'help'
            ]

            combined_text = (user_input + " " + ai_response).lower()
            if any(keyword in combined_text for keyword in important_keywords):
                importance = 7

            # Store the conversation experience
            memory_content = f"Had conversation about: {user_input[:100]}{'...' if len(user_input) > 100 else ''}"
            character.add_memory(memory_content, importance=importance)

    def inject_experience(self, character, experience: str, importance: int = 6):
        """Inject a specific experience that the character can remember and reference."""
        if hasattr(character, 'add_memory'):
            character.add_memory(experience, importance=importance)
            return True
        return False

    def get_character_conversation_history(self, character) -> Dict[str, Any]:
        """Get conversation history for a specific character."""
        character_id = f"{character.name}_{character.job.replace(' ', '_')}"
        return self.ollama_client.get_conversation_summary(character_id)

    def clear_character_conversations(self, character):
        """Clear conversation history for a specific character."""
        character_id = f"{character.name}_{character.job.replace(' ', '_')}"
        self.ollama_client.clear_conversation_history(character_id)

    def test_connection(self) -> bool:
        """Test connection to Ollama server."""
        return self.ollama_client.check_connection()

    def switch_model(self, model_name: str) -> bool:
        """Switch to a different Ollama model."""
        return self.ollama_client.switch_model(model_name)