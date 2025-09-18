from typing import List, Dict, Any
from datetime import datetime
import sqlite3
from pathlib import Path


class World:
    def __init__(self, name: str = "Riverside Town"):
        self.name = name
        self.population = 300
        self.time = datetime.now()
        self.weather = "sunny"
        self.temperature = 72

        self.locations = {
            "riverside": {
                "name": "Riverside Park",
                "description": "A peaceful park along the flowing river with walking trails and benches",
                "occupants": []
            },
            "hospital": {
                "name": "Riverside General Hospital",
                "description": "A modern medical facility serving the town's healthcare needs",
                "occupants": []
            },
            "research_station": {
                "name": "Aquatic Research Station",
                "description": "A research facility studying marine life and river ecosystems",
                "occupants": []
            },
            "town_center": {
                "name": "Town Center",
                "description": "The bustling heart of Riverside Town with shops and cafes",
                "occupants": []
            },
            "marina": {
                "name": "Riverside Marina",
                "description": "A dock area with boats and fishing equipment",
                "occupants": []
            }
        }

        self.ai_characters = []
        self.npcs = []

        self.db_path = Path("world_state.db")
        self._init_database()

    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS world_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                event_type TEXT,
                description TEXT,
                location TEXT,
                participants TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS character_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_name TEXT,
                character_type TEXT,
                location TEXT,
                mood TEXT,
                activity TEXT,
                timestamp TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def add_character(self, character):
        if hasattr(character, 'job') and character.job in ['Deep Sea Researcher', 'ER Surgeon']:
            self.ai_characters.append(character)
        else:
            self.npcs.append(character)

        self.log_event(
            event_type="character_added",
            description=f"{character.name} joined the world",
            location="town_center",
            participants=character.name
        )

    def move_character(self, character, location_key: str):
        if location_key in self.locations:
            for loc in self.locations.values():
                if character in loc["occupants"]:
                    loc["occupants"].remove(character)

            self.locations[location_key]["occupants"].append(character)
            character.location = location_key

            self.log_event(
                event_type="character_movement",
                description=f"{character.name} moved to {self.locations[location_key]['name']}",
                location=location_key,
                participants=character.name
            )

    def log_event(self, event_type: str, description: str, location: str = "", participants: str = ""):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO world_events (timestamp, event_type, description, location, participants)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), event_type, description, location, participants))

        conn.commit()
        conn.close()

    def update_time(self, hours: int = 1):
        from datetime import timedelta
        self.time += timedelta(hours=hours)

        self.log_event(
            event_type="time_update",
            description=f"Time advanced to {self.time.strftime('%Y-%m-%d %H:%M')}",
            location="global"
        )

    def get_location_info(self, location_key: str) -> Dict[str, Any]:
        if location_key in self.locations:
            location = self.locations[location_key].copy()
            location["occupant_names"] = [char.name for char in location["occupants"]]
            return location
        return {}

    def get_world_summary(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "time": self.time.strftime('%Y-%m-%d %H:%M'),
            "weather": self.weather,
            "temperature": self.temperature,
            "total_population": len(self.ai_characters) + len(self.npcs),
            "ai_characters": len(self.ai_characters),
            "npcs": len(self.npcs),
            "locations": list(self.locations.keys())
        }

    def simulate_step(self):
        self.update_time(1)

        for character in self.ai_characters:
            if hasattr(character, 'take_action'):
                character.take_action(self)

        for npc in self.npcs[:10]:  # Simulate first 10 NPCs for performance
            if hasattr(npc, 'take_action'):
                npc.take_action(self)