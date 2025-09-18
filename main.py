#!/usr/bin/env python3
"""
Simulated AI Reality - Main Entry Point

A simulation featuring 2 AI characters (Deep Sea Researcher and ER Surgeon)
living in a riverside town with 300 NPCs.
"""

import sys
import time
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.world.world_state import World
from src.characters.ai_characters import DeepSeaResearcher, ERSurgeon
from src.npcs.npc_manager import NPCManager


def print_banner():
    """Print welcome banner for the simulation."""
    print("=" * 60)
    print("    SIMULATED AI REALITY - RIVERSIDE TOWN")
    print("=" * 60)
    print("Welcome to a living simulation featuring:")
    print("* 2 AI Characters with distinct personalities")
    print("* 300 NPCs with unique traits and daily routines")
    print("* Dynamic world interactions and relationships")
    print("=" * 60)
    print()


def initialize_world():
    """Create and set up the world environment."""
    print("[WORLD] Initializing Riverside Town...")
    world = World("Riverside Town")

    print(f"[OK] Created world: {world.name}")
    print(f"     Locations: {len(world.locations)}")
    print(f"     Time: {world.time.strftime('%Y-%m-%d %H:%M')}")
    print(f"     Weather: {world.weather}, {world.temperature}°F")
    print()

    return world


def create_ai_characters(world):
    """Create and add the two main AI characters."""
    print("[AI] Creating AI Characters...")

    # Create Dr. Marina Depth - Deep Sea Researcher
    researcher = DeepSeaResearcher()
    world.add_character(researcher)

    print(f"[OK] Created {researcher.name}")
    print(f"     Job: {researcher.job}")
    print(f"     Top traits: {', '.join(researcher.get_dominant_traits())}")
    print(f"     Research projects: {len(researcher.research_projects)}")

    # Create Dr. Alex Healer - ER Surgeon
    surgeon = ERSurgeon()
    world.add_character(surgeon)

    print(f"[OK] Created {surgeon.name}")
    print(f"     Job: {surgeon.job}")
    print(f"     Top traits: {', '.join(surgeon.get_dominant_traits())}")
    print(f"     Specializations: {len(surgeon.specializations)}")
    print()

    return researcher, surgeon


def generate_npc_population(world):
    """Generate and distribute 300 NPCs throughout the town."""
    print("[NPCs] Generating NPC Population...")

    npc_manager = NPCManager(target_population=300)

    # Create all 300 NPCs
    print("       Creating 300 unique NPCs with diverse backgrounds...")
    npcs = npc_manager.create_npcs(300)

    # Add NPCs to world
    for npc in npcs:
        world.add_character(npc)

    # Distribute NPCs to appropriate locations
    print("       Distributing NPCs to locations based on preferences...")
    npc_manager.distribute_npcs_to_world(world)

    print(f"[OK] Population Complete!")
    print(f"     Total NPCs: {len(npcs)}")
    print(f"     Unique jobs: {len(set(npc.job for npc in npcs))}")
    print(f"     Personality diversity: 10 traits per NPC")
    print()

    return npc_manager


def display_world_status(world, npc_manager):
    """Show current world status and statistics."""
    print("[STATUS] CURRENT WORLD STATUS")
    print("-" * 40)

    # World summary
    world_summary = world.get_world_summary()
    print(f"World: {world_summary['name']}")
    print(f"Time: {world_summary['time']}")
    print(f"Weather: {world_summary['weather']}, {world_summary['temperature']}°F")
    print(f"Total Population: {world_summary['total_population']}")
    print(f"AI Characters: {world_summary['ai_characters']}")
    print(f"NPCs: {world_summary['npcs']}")
    print()

    # Location distribution
    print("[LOCATIONS] DISTRIBUTION")
    print("-" * 25)
    for location_key, location_data in world.locations.items():
        occupant_count = len(location_data["occupants"])
        print(f"{location_data['name']}: {occupant_count} people")
    print()

    # AI Character status
    print("[AI] CHARACTER STATUS")
    print("-" * 25)
    for ai_char in world.ai_characters:
        char_summary = ai_char.get_character_summary()
        print(f"{char_summary['name']} ({char_summary['job']})")
        print(f"   Location: {world.locations[char_summary['location']]['name']}")
        print(f"   Mood: {char_summary['mood']}")
        print(f"   Energy: {char_summary['energy']}%")
        print(f"   Activity: {char_summary['current_activity']}")

        # Show profession-specific stats
        if hasattr(ai_char, 'get_research_summary'):
            research = ai_char.get_research_summary()
            print(f"   Samples collected: {research['samples_collected']}")
            print(f"   Discoveries: {research['discoveries_made']}")
        elif hasattr(ai_char, 'get_medical_summary'):
            medical = ai_char.get_medical_summary()
            print(f"   Patients treated: {medical['patients_treated']}")
            print(f"   Surgeries: {medical['surgeries_performed']}")
        print()

    # Population insights
    pop_summary = npc_manager.get_population_summary()
    print("[POPULATION] INSIGHTS")
    print("-" * 25)
    print(f"Population completion: {pop_summary['population_overview']['completion_percentage']}%")
    print(f"Job diversity: {pop_summary['demographics']['job_diversity']} different professions")
    print(f"Social connections: {pop_summary['social_dynamics']['total_relationships']} relationships")
    print(f"Highly social NPCs: {pop_summary['social_dynamics']['highly_social_npcs']}")
    print()


def run_simulation_step(world, npc_manager, step_num):
    """Run one step of the simulation."""
    print(f"[STEP {step_num}] Simulation Step")
    print("-" * 30)

    # Advance world time
    world.simulate_step()

    # Simulate NPC interactions (50 random NPCs per step for performance)
    npc_manager.simulate_npc_interactions(world, active_npcs=50)

    # Show some activity highlights
    recent_events = []

    # AI character activities
    for ai_char in world.ai_characters:
        if ai_char.current_activity != "idle":
            recent_events.append(f"[AI] {ai_char.name}: {ai_char.current_activity}")

    # Sample NPC activities
    active_npcs = npc_manager.get_random_npcs(5)
    for npc in active_npcs:
        if npc.current_activity != "idle":
            recent_events.append(f"[NPC] {npc.name} ({npc.job}): {npc.current_activity}")

    if recent_events:
        print("Recent activities:")
        for event in recent_events[:8]:  # Show max 8 activities
            print(f"   {event}")
    else:
        print("   Peaceful moment in Riverside Town...")

    print(f"Current time: {world.time.strftime('%H:%M')}")
    print()


def main():
    """Main simulation entry point."""
    try:
        # Display welcome banner
        print_banner()

        # Initialize the world
        world = initialize_world()

        # Create AI characters
        researcher, surgeon = create_ai_characters(world)

        # Generate NPC population
        npc_manager = generate_npc_population(world)

        # Show initial world status
        display_world_status(world, npc_manager)

        # Demonstrate the simulation is working
        print("[DEMO] SIMULATION DEMONSTRATION")
        print("=" * 40)
        print("Running 5 simulation steps to show the world in action...")
        print()

        for step in range(1, 6):
            run_simulation_step(world, npc_manager, step)
            time.sleep(1)  # Brief pause between steps

        print("[SUCCESS] SIMULATION FOUNDATION COMPLETE!")
        print("=" * 50)
        print("Successfully created:")
        print(f"   * World with {len(world.locations)} locations")
        print(f"   * 2 AI characters with unique personalities")
        print(f"   * 300 NPCs with diverse backgrounds and routines")
        print(f"   * Dynamic interaction and event logging system")
        print(f"   * SQLite database: {world.db_path}")
        print()
        print("The foundation is ready for your AI reality simulation!")
        print("You can now extend this with:")
        print("   * AI character conversations and decision making")
        print("   * Complex NPC social networks and relationships")
        print("   * World events and dynamic story generation")
        print("   * Integration with language models for character AI")

    except KeyboardInterrupt:
        print("\n[STOP] Simulation interrupted by user")

    except Exception as e:
        print(f"\n[ERROR] Error running simulation: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()