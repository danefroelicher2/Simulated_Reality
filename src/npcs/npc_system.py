from typing import List, Dict, Any, Optional
import random
from ..characters.base_character import BaseCharacter, PersonalityTraits


class NPC(BaseCharacter):
    def __init__(
        self,
        name: str,
        job: str,
        age: int = None,
        background: str = ""
    ):
        personality_traits = self._generate_random_personality()

        if age is None:
            age = random.randint(18, 75)

        if not background:
            background = self._generate_background(job)

        super().__init__(
            name=name,
            job=job,
            personality_traits=personality_traits,
            age=age,
            background=background
        )

        self.npc_type = "townsperson"
        self.daily_routine = self._generate_daily_routine()
        self.preferred_locations = self._get_preferred_locations()
        self.social_circle = []
        self.work_schedule = self._generate_work_schedule()

    def _generate_random_personality(self) -> PersonalityTraits:
        traits = {}
        trait_names = [
            "curiosity", "empathy", "confidence", "creativity", "analytical",
            "social", "cautious", "ambitious", "humor", "adaptability"
        ]

        remaining_points = 100
        for i, trait in enumerate(trait_names):
            if i == len(trait_names) - 1:
                traits[trait] = remaining_points
            else:
                min_points = 0
                max_points = min(remaining_points, 30)
                points = random.randint(min_points, max_points)
                traits[trait] = points
                remaining_points -= points

        return PersonalityTraits(**traits)

    def _generate_background(self, job: str) -> str:
        backgrounds = {
            "shopkeeper": "Runs a small family business that has been in the town for generations",
            "teacher": "Dedicated educator who moved to the riverside town for its peaceful environment",
            "fisherman": "Local who knows every spot along the river and its seasonal patterns",
            "chef": "Culinary artist who specializes in fresh river fish and local ingredients",
            "librarian": "Quiet intellectual who maintains the town's historical records and stories",
            "mechanic": "Skilled tradesperson who repairs everything from boats to bicycles",
            "artist": "Creative soul inspired by the natural beauty of the riverside setting",
            "farmer": "Agricultural worker who grows crops in the fertile riverbank soil",
            "postal_worker": "Connects the town to the outside world through mail and packages",
            "security_guard": "Protects local businesses and ensures community safety",
            "cafe_owner": "Social hub creator who knows everyone's coffee preferences and gossip",
            "boat_captain": "River transportation expert who ferries people and goods",
            "gardener": "Green thumb who maintains the town's parks and public spaces",
            "carpenter": "Skilled craftsperson who builds and repairs the town's wooden structures",
            "journalist": "Local news gatherer who documents the town's daily happenings"
        }

        return backgrounds.get(job, f"Local resident working as a {job} in the riverside community")

    def _generate_daily_routine(self) -> List[Dict[str, Any]]:
        routine = []

        work_hours = random.randint(6, 10)
        start_time = random.randint(6, 9)

        routine.append({
            "time": f"{start_time}:00",
            "activity": "work",
            "location": self._get_work_location(),
            "duration": work_hours
        })

        lunch_time = start_time + (work_hours // 2)
        routine.append({
            "time": f"{lunch_time}:00",
            "activity": "lunch_break",
            "location": "town_center",
            "duration": 1
        })

        if random.random() > 0.7:
            routine.append({
                "time": f"{start_time + work_hours + 1}:00",
                "activity": "social_time",
                "location": random.choice(["town_center", "riverside"]),
                "duration": 2
            })

        routine.append({
            "time": f"{start_time + work_hours + 3}:00",
            "activity": "personal_time",
            "location": "home",
            "duration": 3
        })

        return routine

    def _get_work_location(self) -> str:
        work_locations = {
            "shopkeeper": "town_center",
            "teacher": "town_center",
            "fisherman": "riverside",
            "chef": "town_center",
            "librarian": "town_center",
            "mechanic": "town_center",
            "artist": "riverside",
            "farmer": "riverside",
            "postal_worker": "town_center",
            "security_guard": "town_center",
            "cafe_owner": "town_center",
            "boat_captain": "marina",
            "gardener": "riverside",
            "carpenter": "town_center",
            "journalist": "town_center"
        }
        return work_locations.get(self.job, "town_center")

    def _get_preferred_locations(self) -> List[str]:
        if self.personality.social >= 20:
            return ["town_center", "riverside", "marina"]
        elif self.personality.curiosity >= 20:
            return ["research_station", "riverside", "town_center"]
        elif self.personality.cautious >= 20:
            return ["town_center", "hospital"]
        else:
            return ["riverside", "town_center"]

    def _generate_work_schedule(self) -> Dict[str, bool]:
        if self.job in ["fisherman", "farmer", "gardener"]:
            return {
                "monday": True, "tuesday": True, "wednesday": True,
                "thursday": True, "friday": True, "saturday": True, "sunday": False
            }
        elif self.job in ["teacher", "librarian", "postal_worker"]:
            return {
                "monday": True, "tuesday": True, "wednesday": True,
                "thursday": True, "friday": True, "saturday": False, "sunday": False
            }
        else:
            return {
                "monday": True, "tuesday": True, "wednesday": True,
                "thursday": True, "friday": True,
                "saturday": random.choice([True, False]),
                "sunday": random.choice([True, False])
            }

    def get_possible_actions(self, world) -> List[str]:
        base_actions = super().get_possible_actions(world)

        npc_actions = [
            "work_at_job",
            "chat_with_neighbors",
            "shop_for_supplies",
            "enjoy_hobby",
            "visit_family",
            "attend_community_event",
            "help_neighbor",
            "take_walk",
            "read_local_news",
            "maintain_home"
        ]

        job_specific_actions = {
            "fisherman": ["cast_fishing_line", "repair_nets", "sell_fish"],
            "shopkeeper": ["serve_customers", "restock_inventory", "count_register"],
            "teacher": ["prepare_lessons", "grade_papers", "tutor_students"],
            "chef": ["prepare_meals", "shop_for_ingredients", "experiment_recipes"],
            "artist": ["paint_landscape", "sketch_people", "sell_artwork"],
            "farmer": ["tend_crops", "feed_animals", "harvest_produce"],
            "mechanic": ["repair_vehicles", "order_parts", "maintain_tools"],
            "librarian": ["organize_books", "help_patrons", "read_quietly"],
            "boat_captain": ["check_boat_engine", "navigate_river", "transport_passengers"],
            "gardener": ["water_plants", "prune_trees", "plant_flowers"]
        }

        if self.job in job_specific_actions:
            npc_actions.extend(job_specific_actions[self.job])

        location_actions = {
            "riverside": ["watch_sunset", "feed_ducks", "collect_river_stones"],
            "town_center": ["window_shop", "people_watch", "buy_newspaper"],
            "hospital": ["visit_doctor", "volunteer_help"],
            "marina": ["admire_boats", "talk_to_sailors"],
            "research_station": ["ask_about_research", "observe_scientists"]
        }

        if self.location in location_actions:
            npc_actions.extend(location_actions[self.location])

        return base_actions + npc_actions

    def execute_action(self, action: str, world):
        super().execute_action(action, world)

        if action == "work_at_job":
            work_location = self._get_work_location()
            if self.location != work_location:
                world.move_character(self, work_location)

            self.set_activity(f"working as {self.job}")
            self.add_memory(f"Completed work duties as {self.job}", importance=4)

        elif action == "chat_with_neighbors":
            location_occupants = world.locations[self.location]["occupants"]
            other_people = [char for char in location_occupants if char != self]

            if other_people:
                chat_partner = random.choice(other_people)
                topic = random.choice([
                    "weather", "local_news", "family", "work", "hobbies",
                    "river_conditions", "town_events", "fishing_spots"
                ])

                self.add_memory(f"Had a nice chat with {chat_partner.name} about {topic}", importance=5)

                if chat_partner.name not in self.relationships:
                    self.add_relationship(chat_partner.name, "neighbor", random.randint(40, 70))

                world.log_event(
                    event_type="social_interaction",
                    description=f"{self.name} chatted with {chat_partner.name} about {topic}",
                    location=self.location,
                    participants=f"{self.name}, {chat_partner.name}"
                )

        elif action == "attend_community_event":
            event_types = [
                "town_meeting", "festival", "market_day", "concert",
                "art_show", "book_reading", "fishing_competition"
            ]
            event = random.choice(event_types)
            self.add_memory(f"Attended {event} - met some interesting people", importance=6)
            world.log_event(
                event_type="community_event",
                description=f"{self.name} attended {event}",
                location=self.location,
                participants=self.name
            )

        elif action in ["cast_fishing_line", "paint_landscape", "tend_crops"]:
            skill_gain = random.randint(1, 3)
            self.add_memory(f"Practiced {action} and improved my skills", importance=4)
            world.log_event(
                event_type="skill_development",
                description=f"{self.name} practiced {action}",
                location=self.location,
                participants=self.name
            )

    def get_npc_summary(self) -> Dict[str, Any]:
        base_summary = self.get_character_summary()
        npc_summary = {
            "npc_type": self.npc_type,
            "work_location": self._get_work_location(),
            "daily_routine_length": len(self.daily_routine),
            "preferred_locations": self.preferred_locations,
            "social_connections": len(self.relationships),
            "work_days_per_week": sum(self.work_schedule.values())
        }

        return {**base_summary, **npc_summary}

    def follow_routine(self, world, current_hour: int):
        for routine_item in self.daily_routine:
            routine_hour = int(routine_item["time"].split(":")[0])
            if routine_hour == current_hour:
                target_location = routine_item["location"]
                if target_location != "home" and target_location in world.locations:
                    world.move_character(self, target_location)

                self.set_activity(routine_item["activity"])
                break