from typing import List, Dict, Any, Optional
import random
from .npc_system import NPC


class NPCManager:
    def __init__(self, target_population: int = 300):
        self.target_population = target_population
        self.npcs: List[NPC] = []
        self.npc_database: Dict[str, NPC] = {}
        self.job_distribution = self._create_job_distribution()
        self.name_pools = self._create_name_pools()
        self.population_stats = {}

    def _create_job_distribution(self) -> Dict[str, int]:
        return {
            "shopkeeper": 15,
            "fisherman": 25,
            "farmer": 20,
            "chef": 8,
            "teacher": 12,
            "mechanic": 10,
            "librarian": 3,
            "artist": 12,
            "postal_worker": 4,
            "security_guard": 6,
            "cafe_owner": 5,
            "boat_captain": 8,
            "gardener": 10,
            "carpenter": 12,
            "journalist": 3,
            "bartender": 8,
            "baker": 6,
            "musician": 8,
            "photographer": 4,
            "delivery_driver": 7,
            "store_clerk": 18,
            "tour_guide": 5,
            "veterinarian": 2,
            "electrician": 6,
            "plumber": 4,
            "taxi_driver": 6,
            "florist": 3,
            "jeweler": 2,
            "tailor": 4,
            "barber": 5,
            "accountant": 3,
            "real_estate_agent": 4,
            "insurance_agent": 3,
            "bank_teller": 4,
            "mailroom_clerk": 3,
            "janitor": 8,
            "receptionist": 6,
            "waitress": 12,
            "cashier": 15,
            "sales_associate": 10,
            "landscaper": 8,
            "construction_worker": 12,
            "handyman": 8,
            "maintenance_worker": 6,
            "dock_worker": 10,
            "warehouse_worker": 8
        }

    def _create_name_pools(self) -> Dict[str, List[str]]:
        return {
            "first_names": [
                "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Avery", "Quinn",
                "Sage", "River", "Rowan", "Blake", "Cameron", "Dakota", "Emery", "Finley",
                "Harper", "Hayden", "Jamie", "Kai", "Lane", "Logan", "Parker", "Peyton",
                "Reese", "Skylar", "Sydney", "Adrian", "Ashton", "Bailey", "Charlie",
                "Drew", "Ellis", "Evren", "Gray", "Hunter", "Iris", "Jules", "Kennedy",
                "Lee", "Marlowe", "Nico", "Ocean", "Phoenix", "Rain", "Sam", "Tatum",
                "Val", "Winter", "Zara", "Brook", "Clay", "Eden", "Fox", "Glen",
                "Hope", "Indigo", "Jade", "Knox", "Lake", "Moon", "North", "Onyx",
                "Pine", "Quill", "Reed", "Stone", "Teal", "Uma", "Vale", "Wade",
                "Wren", "York", "Zion", "Ash", "Bay", "Coral", "Dell", "Echo",
                "Fern", "Grove", "Heath", "Isle", "Jasper", "Lark", "Mesa", "Nova",
                "Oak", "Pearl", "Sage", "Terra", "Unity", "Vega", "Wilde", "Zen",
                "Abel", "Beau", "Cove", "Dean", "Eli", "Finn", "Gage", "Hart",
                "Ivan", "Jude", "Knox", "Liam", "Max", "Noah", "Owen", "Paul",
                "Quinn", "Ryan", "Sean", "Troy", "Uma", "Vince", "Will", "Xander",
                "Yael", "Zoe", "Aria", "Beth", "Cora", "Dana", "Eva", "Faith",
                "Grace", "Hana", "Ivy", "Joy", "Kate", "Luna", "Maya", "Nora",
                "Olive", "Piper", "Rose", "Sara", "Tara", "Uma", "Vera", "Willow"
            ],
            "last_names": [
                "Rivers", "Brooks", "Waters", "Banks", "Fisher", "Stone", "Reed",
                "Field", "Grove", "Hill", "Dale", "Vale", "Creek", "Shore", "Bay",
                "Harbor", "Dock", "Bridge", "Ford", "Mill", "Wells", "Springs",
                "Falls", "Rapids", "Current", "Stream", "Flow", "Tide", "Wave",
                "Marsh", "Pond", "Lake", "Ocean", "Sea", "Coast", "Beach", "Cliff",
                "Rock", "Sand", "Pearl", "Shell", "Coral", "Marina", "Port",
                "Anchor", "Sail", "Boat", "Ship", "Float", "Drift", "Wade",
                "Swim", "Dive", "Catch", "Net", "Hook", "Line", "Cast", "Reel",
                "Bass", "Trout", "Pike", "Carp", "Salmon", "Cod", "Sole", "Perch",
                "Willow", "Oak", "Pine", "Birch", "Maple", "Cedar", "Elm", "Ash",
                "Fern", "Moss", "Ivy", "Rose", "Lily", "Daisy", "Violet", "Iris",
                "Garden", "Bloom", "Petal", "Leaf", "Branch", "Root", "Seed",
                "Berry", "Apple", "Cherry", "Plum", "Peach", "Grape", "Orange",
                "Lemon", "Mint", "Sage", "Basil", "Thyme", "Rosemary", "Lavender",
                "Craft", "Smith", "Wright", "Wood", "Clay", "Glass", "Metal",
                "Gold", "Silver", "Copper", "Iron", "Steel", "Bronze", "Brass"
            ]
        }

    def generate_random_name(self) -> str:
        first_name = random.choice(self.name_pools["first_names"])
        last_name = random.choice(self.name_pools["last_names"])
        return f"{first_name} {last_name}"

    def create_npcs(self, count: int = None) -> List[NPC]:
        if count is None:
            count = self.target_population

        jobs_to_create = []
        for job, quantity in self.job_distribution.items():
            jobs_to_create.extend([job] * quantity)

        while len(jobs_to_create) < count:
            additional_job = random.choice(list(self.job_distribution.keys()))
            jobs_to_create.append(additional_job)

        random.shuffle(jobs_to_create)
        jobs_to_create = jobs_to_create[:count]

        created_npcs = []
        used_names = set()

        for i, job in enumerate(jobs_to_create):
            name = self.generate_random_name()
            while name in used_names:
                name = self.generate_random_name()
            used_names.add(name)

            npc = NPC(name=name, job=job)
            created_npcs.append(npc)
            self.npc_database[name] = npc

        self.npcs.extend(created_npcs)
        self._update_population_stats()

        return created_npcs

    def _update_population_stats(self):
        self.population_stats = {
            "total_npcs": len(self.npcs),
            "job_counts": {},
            "age_distribution": {"18-30": 0, "31-45": 0, "46-60": 0, "61-75": 0},
            "personality_averages": {
                "curiosity": 0, "empathy": 0, "confidence": 0, "creativity": 0,
                "analytical": 0, "social": 0, "cautious": 0, "ambitious": 0,
                "humor": 0, "adaptability": 0
            },
            "location_distribution": {}
        }

        for npc in self.npcs:
            job = npc.job
            self.population_stats["job_counts"][job] = self.population_stats["job_counts"].get(job, 0) + 1

            age = npc.age
            if 18 <= age <= 30:
                self.population_stats["age_distribution"]["18-30"] += 1
            elif 31 <= age <= 45:
                self.population_stats["age_distribution"]["31-45"] += 1
            elif 46 <= age <= 60:
                self.population_stats["age_distribution"]["46-60"] += 1
            elif 61 <= age <= 75:
                self.population_stats["age_distribution"]["61-75"] += 1

            location = npc.location
            self.population_stats["location_distribution"][location] = \
                self.population_stats["location_distribution"].get(location, 0) + 1

        if self.npcs:
            total_npcs = len(self.npcs)
            for trait in self.population_stats["personality_averages"]:
                total_trait_value = sum(getattr(npc.personality, trait) for npc in self.npcs)
                self.population_stats["personality_averages"][trait] = round(total_trait_value / total_npcs, 1)

    def get_npcs_by_job(self, job: str) -> List[NPC]:
        return [npc for npc in self.npcs if npc.job == job]

    def get_npcs_by_location(self, location: str) -> List[NPC]:
        return [npc for npc in self.npcs if npc.location == location]

    def get_npcs_by_trait(self, trait: str, min_value: int = 20) -> List[NPC]:
        return [npc for npc in self.npcs if getattr(npc.personality, trait) >= min_value]

    def get_social_npcs(self, min_social: int = 15) -> List[NPC]:
        return self.get_npcs_by_trait("social", min_social)

    def find_npc_by_name(self, name: str) -> Optional[NPC]:
        return self.npc_database.get(name)

    def get_random_npcs(self, count: int = 10) -> List[NPC]:
        return random.sample(self.npcs, min(count, len(self.npcs)))

    def simulate_npc_interactions(self, world, active_npcs: int = 50):
        active_group = random.sample(self.npcs, min(active_npcs, len(self.npcs)))

        for npc in active_group:
            if random.random() < 0.3:
                npc.take_action(world)

        current_hour = world.time.hour
        for npc in active_group:
            if random.random() < 0.7:
                npc.follow_routine(world, current_hour)

    def get_population_summary(self) -> Dict[str, Any]:
        self._update_population_stats()
        return {
            "population_overview": {
                "total_npcs": self.population_stats["total_npcs"],
                "target_population": self.target_population,
                "completion_percentage": round((self.population_stats["total_npcs"] / self.target_population) * 100, 1)
            },
            "demographics": {
                "age_distribution": self.population_stats["age_distribution"],
                "job_diversity": len(self.population_stats["job_counts"]),
                "most_common_jobs": sorted(
                    self.population_stats["job_counts"].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
            },
            "personality_profile": self.population_stats["personality_averages"],
            "location_spread": self.population_stats["location_distribution"],
            "social_dynamics": {
                "highly_social_npcs": len(self.get_social_npcs(20)),
                "total_relationships": sum(len(npc.relationships) for npc in self.npcs),
                "average_relationships_per_npc": round(
                    sum(len(npc.relationships) for npc in self.npcs) / max(len(self.npcs), 1), 1
                )
            }
        }

    def distribute_npcs_to_world(self, world):
        locations = list(world.locations.keys())

        for npc in self.npcs:
            if npc.location == "town_center":
                preferred_location = random.choice(npc.preferred_locations)
                if preferred_location in locations:
                    world.move_character(npc, preferred_location)
                else:
                    world.move_character(npc, random.choice(locations))

        world.log_event(
            event_type="population_distribution",
            description=f"Distributed {len(self.npcs)} NPCs across the world",
            location="global",
            participants=f"{len(self.npcs)} NPCs"
        )

    def reset_npcs(self):
        self.npcs.clear()
        self.npc_database.clear()
        self.population_stats.clear()