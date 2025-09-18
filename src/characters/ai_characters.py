from .base_character import BaseCharacter, PersonalityTraits
from typing import List, Dict, Any
import random


class DeepSeaResearcher(BaseCharacter):
    def __init__(
        self,
        name: str = "Dr. Marina Depth",
        age: int = 35,
        background: str = "Marine biologist with 10 years of deep sea exploration experience"
    ):
        researcher_traits = PersonalityTraits(
            curiosity=25,
            empathy=12,
            confidence=15,
            creativity=18,
            analytical=20,
            social=5,
            cautious=3,
            ambitious=2,
            humor=0,
            adaptability=0
        )

        super().__init__(
            name=name,
            job="Deep Sea Researcher",
            personality_traits=researcher_traits,
            age=age,
            background=background
        )

        self.skills = {
            "marine_biology": 95,
            "deep_sea_diving": 90,
            "research_methodology": 85,
            "data_analysis": 88,
            "equipment_operation": 92,
            "underwater_photography": 80
        }

        self.research_projects = [
            "Bioluminescent organisms in river ecosystems",
            "Impact of water temperature on fish migration patterns",
            "Microplastic contamination in freshwater systems"
        ]

        self.equipment = [
            "underwater_camera",
            "water_quality_sensors",
            "sample_collection_kit",
            "diving_gear",
            "microscope"
        ]

        self.discoveries = []
        self.samples_collected = 0

        self.goals = [
            "Complete comprehensive study of river ecosystem",
            "Publish research on local aquatic biodiversity",
            "Discover new species in the river system"
        ]

        self.location = "research_station"

    def get_possible_actions(self, world) -> List[str]:
        base_actions = super().get_possible_actions(world)

        researcher_actions = [
            "collect_water_samples",
            "analyze_specimens",
            "document_findings",
            "calibrate_equipment",
            "plan_dive_expedition",
            "review_research_data",
            "prepare_dive_equipment",
            "study_water_currents",
            "photograph_specimens",
            "update_field_notes"
        ]

        if self.location == "riverside":
            researcher_actions.extend([
                "dive_for_samples",
                "test_water_quality",
                "observe_fish_behavior",
                "map_underwater_terrain"
            ])
        elif self.location == "research_station":
            researcher_actions.extend([
                "use_laboratory_equipment",
                "process_samples",
                "write_research_report",
                "video_conference_with_colleagues"
            ])

        return base_actions + researcher_actions

    def execute_action(self, action: str, world):
        super().execute_action(action, world)

        if action == "collect_water_samples":
            self.samples_collected += random.randint(1, 3)
            self.add_memory(f"Collected water samples. Total samples: {self.samples_collected}", importance=6)
            world.log_event(
                event_type="research_activity",
                description=f"{self.name} collected water samples",
                location=self.location,
                participants=self.name
            )

        elif action == "analyze_specimens":
            if self.samples_collected > 0:
                discovery_chance = random.random()
                if discovery_chance > 0.7:
                    discovery = f"Unusual {random.choice(['algae', 'bacteria', 'microorganism'])} strain"
                    self.discoveries.append(discovery)
                    self.add_memory(f"Made exciting discovery: {discovery}!", importance=9)
                    world.log_event(
                        event_type="scientific_discovery",
                        description=f"{self.name} discovered: {discovery}",
                        location=self.location,
                        participants=self.name
                    )

        elif action == "dive_for_samples":
            if self.location == "riverside":
                self.samples_collected += random.randint(2, 5)
                depth_explored = random.randint(10, 30)
                self.add_memory(f"Dove to {depth_explored}m depth, collected valuable samples", importance=7)
                world.log_event(
                    event_type="field_research",
                    description=f"{self.name} conducted deep dive research",
                    location=self.location,
                    participants=self.name
                )

        elif action == "document_findings":
            if self.discoveries:
                self.add_memory("Documented recent findings for publication", importance=8)
                world.log_event(
                    event_type="research_documentation",
                    description=f"{self.name} documented research findings",
                    location=self.location,
                    participants=self.name
                )

    def get_research_summary(self) -> Dict[str, Any]:
        return {
            "active_projects": len(self.research_projects),
            "samples_collected": self.samples_collected,
            "discoveries_made": len(self.discoveries),
            "recent_discoveries": self.discoveries[-3:] if self.discoveries else [],
            "research_skills": self.skills,
            "preferred_location": "research_station"
        }


class ERSurgeon(BaseCharacter):
    def __init__(
        self,
        name: str = "Dr. Alex Healer",
        age: int = 42,
        background: str = "Emergency medicine specialist with 15 years of trauma surgery experience"
    ):
        surgeon_traits = PersonalityTraits(
            curiosity=10,
            empathy=25,
            confidence=20,
            creativity=8,
            analytical=15,
            social=12,
            cautious=5,
            ambitious=3,
            humor=2,
            adaptability=0
        )

        super().__init__(
            name=name,
            job="ER Surgeon",
            personality_traits=surgeon_traits,
            age=age,
            background=background
        )

        self.skills = {
            "emergency_surgery": 95,
            "trauma_care": 92,
            "patient_diagnosis": 90,
            "medical_procedures": 88,
            "crisis_management": 85,
            "patient_communication": 80
        }

        self.specializations = [
            "Trauma surgery",
            "Emergency cardiac procedures",
            "Pediatric emergency care",
            "Disaster medicine"
        ]

        self.equipment = [
            "surgical_instruments",
            "stethoscope",
            "medical_scanner",
            "emergency_medication",
            "defibrillator"
        ]

        self.patients_treated = 0
        self.surgeries_performed = 0
        self.medical_cases = []

        self.goals = [
            "Maintain zero patient mortality rate",
            "Train junior medical staff",
            "Improve emergency response protocols"
        ]

        self.location = "hospital"

    def get_possible_actions(self, world) -> List[str]:
        base_actions = super().get_possible_actions(world)

        surgeon_actions = [
            "examine_patients",
            "perform_surgery",
            "review_medical_charts",
            "consult_specialists",
            "train_medical_staff",
            "update_patient_records",
            "check_emergency_supplies",
            "practice_procedures",
            "attend_medical_conference",
            "research_medical_literature"
        ]

        if self.location == "hospital":
            surgeon_actions.extend([
                "rounds_with_patients",
                "emergency_response_drill",
                "mentor_residents",
                "equipment_maintenance"
            ])
        elif self.location == "town_center":
            surgeon_actions.extend([
                "provide_first_aid",
                "health_education_outreach",
                "emergency_response"
            ])

        return base_actions + surgeon_actions

    def execute_action(self, action: str, world):
        super().execute_action(action, world)

        if action == "examine_patients":
            patients_seen = random.randint(1, 4)
            self.patients_treated += patients_seen
            self.add_memory(f"Examined {patients_seen} patients today", importance=6)
            world.log_event(
                event_type="medical_care",
                description=f"{self.name} examined {patients_seen} patients",
                location=self.location,
                participants=self.name
            )

        elif action == "perform_surgery":
            surgery_type = random.choice([
                "appendectomy", "trauma_repair", "cardiac_procedure", "emergency_surgery"
            ])
            self.surgeries_performed += 1
            complexity = random.choice(["routine", "complex", "critical"])

            case_record = {
                "type": surgery_type,
                "complexity": complexity,
                "outcome": "successful",
                "timestamp": self.last_action_time
            }
            self.medical_cases.append(case_record)

            self.add_memory(f"Successfully performed {complexity} {surgery_type}", importance=9)
            world.log_event(
                event_type="medical_surgery",
                description=f"{self.name} performed {surgery_type}",
                location=self.location,
                participants=self.name
            )

        elif action == "train_medical_staff":
            topic = random.choice([
                "emergency_protocols", "surgical_techniques", "patient_care", "crisis_management"
            ])
            self.add_memory(f"Conducted training session on {topic}", importance=7)
            world.log_event(
                event_type="medical_training",
                description=f"{self.name} trained staff on {topic}",
                location=self.location,
                participants=self.name
            )

        elif action == "emergency_response":
            emergency_type = random.choice([
                "cardiac_arrest", "severe_trauma", "allergic_reaction", "stroke"
            ])
            self.add_memory(f"Responded to {emergency_type} emergency", importance=8)
            world.log_event(
                event_type="emergency_response",
                description=f"{self.name} responded to {emergency_type}",
                location=self.location,
                participants=self.name
            )

    def get_medical_summary(self) -> Dict[str, Any]:
        return {
            "patients_treated": self.patients_treated,
            "surgeries_performed": self.surgeries_performed,
            "recent_cases": self.medical_cases[-5:] if self.medical_cases else [],
            "specializations": self.specializations,
            "medical_skills": self.skills,
            "preferred_location": "hospital"
        }