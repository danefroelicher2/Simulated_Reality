from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import random


class PersonalityTraits(BaseModel):
    curiosity: int = Field(ge=0, le=100, description="How curious and inquisitive the character is")
    empathy: int = Field(ge=0, le=100, description="How much they care about others")
    confidence: int = Field(ge=0, le=100, description="Self-assurance and boldness")
    creativity: int = Field(ge=0, le=100, description="Innovative and artistic thinking")
    analytical: int = Field(ge=0, le=100, description="Logical and systematic thinking")
    social: int = Field(ge=0, le=100, description="How much they enjoy social interaction")
    cautious: int = Field(ge=0, le=100, description="How careful and risk-averse they are")
    ambitious: int = Field(ge=0, le=100, description="Drive for achievement and success")
    humor: int = Field(ge=0, le=100, description="Appreciation for and use of humor")
    adaptability: int = Field(ge=0, le=100, description="Ability to adjust to new situations")

    def model_post_init(self, __context):
        total = sum([
            self.curiosity, self.empathy, self.confidence, self.creativity,
            self.analytical, self.social, self.cautious, self.ambitious,
            self.humor, self.adaptability
        ])
        if total != 100:
            raise ValueError(f"Personality traits must sum to 100, got {total}")


class BaseCharacter:
    def __init__(
        self,
        name: str,
        job: str,
        personality_traits: PersonalityTraits,
        age: int = 30,
        background: str = ""
    ):
        self.name = name
        self.job = job
        self.age = age
        self.background = background
        self.personality = personality_traits

        self.location = "town_center"
        self.mood = "neutral"
        self.energy = 100
        self.current_activity = "idle"
        self.relationships = {}

        self.memories = []
        self.goals = []
        self.skills = {}

        self.created_at = datetime.now()
        self.last_action_time = datetime.now()

    def get_dominant_traits(self, top_n: int = 3) -> List[str]:
        trait_dict = {
            "curiosity": self.personality.curiosity,
            "empathy": self.personality.empathy,
            "confidence": self.personality.confidence,
            "creativity": self.personality.creativity,
            "analytical": self.personality.analytical,
            "social": self.personality.social,
            "cautious": self.personality.cautious,
            "ambitious": self.personality.ambitious,
            "humor": self.personality.humor,
            "adaptability": self.personality.adaptability
        }

        sorted_traits = sorted(trait_dict.items(), key=lambda x: x[1], reverse=True)
        return [trait[0] for trait in sorted_traits[:top_n]]

    def add_memory(self, memory: str, importance: int = 5):
        self.memories.append({
            "content": memory,
            "timestamp": datetime.now(),
            "importance": importance
        })

        if len(self.memories) > 50:
            self.memories = sorted(self.memories, key=lambda x: x["importance"], reverse=True)[:50]

    def add_relationship(self, character_name: str, relationship_type: str, strength: int = 50):
        self.relationships[character_name] = {
            "type": relationship_type,
            "strength": strength,
            "created": datetime.now()
        }

    def update_mood(self, mood: str):
        self.mood = mood
        self.add_memory(f"My mood changed to {mood}", importance=3)

    def set_activity(self, activity: str):
        self.current_activity = activity
        self.last_action_time = datetime.now()

    def take_action(self, world):
        possible_actions = self.get_possible_actions(world)
        if possible_actions:
            action = self.choose_action(possible_actions)
            self.execute_action(action, world)

    def get_possible_actions(self, world) -> List[str]:
        actions = ["rest", "explore", "socialize"]

        if self.job == "Deep Sea Researcher":
            actions.extend(["research", "collect_samples", "analyze_data"])
        elif self.job == "ER Surgeon":
            actions.extend(["treat_patients", "study_medical_texts", "emergency_response"])

        if self.location == "riverside":
            actions.extend(["fish", "walk_trails", "enjoy_nature"])
        elif self.location == "hospital":
            actions.extend(["visit_patients", "consult_colleagues"])
        elif self.location == "research_station":
            actions.extend(["conduct_research", "use_equipment"])

        return actions

    def choose_action(self, possible_actions: List[str]) -> str:
        trait_weights = {}

        for action in possible_actions:
            weight = 1

            if action in ["research", "analyze_data", "conduct_research"]:
                weight += self.personality.curiosity * 0.02 + self.personality.analytical * 0.02
            elif action in ["socialize", "visit_patients"]:
                weight += self.personality.social * 0.02 + self.personality.empathy * 0.02
            elif action == "explore":
                weight += self.personality.curiosity * 0.02 + self.personality.adaptability * 0.02
            elif action == "rest":
                weight += (100 - self.energy) * 0.01

            trait_weights[action] = max(weight, 0.1)

        total_weight = sum(trait_weights.values())
        choice = random.uniform(0, total_weight)

        current_weight = 0
        for action, weight in trait_weights.items():
            current_weight += weight
            if choice <= current_weight:
                return action

        return random.choice(possible_actions)

    def execute_action(self, action: str, world):
        self.set_activity(action)

        if action == "rest":
            self.energy = min(100, self.energy + 20)
            self.add_memory(f"I rested and feel more energetic", importance=2)

        elif action == "explore":
            locations = list(world.locations.keys())
            new_location = random.choice([loc for loc in locations if loc != self.location])
            world.move_character(self, new_location)
            self.add_memory(f"I explored and moved to {world.locations[new_location]['name']}", importance=4)

        elif action == "socialize":
            location_occupants = world.locations[self.location]["occupants"]
            if len(location_occupants) > 1:
                other_chars = [char for char in location_occupants if char != self]
                if other_chars:
                    partner = random.choice(other_chars)
                    self.add_memory(f"I socialized with {partner.name}", importance=5)
                    if partner.name not in self.relationships:
                        self.add_relationship(partner.name, "acquaintance", 30)

        self.energy = max(0, self.energy - 5)

    def get_character_summary(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "job": self.job,
            "age": self.age,
            "location": self.location,
            "mood": self.mood,
            "energy": self.energy,
            "current_activity": self.current_activity,
            "dominant_traits": self.get_dominant_traits(),
            "relationships": len(self.relationships),
            "memories": len(self.memories)
        }