import json
import datetime
import random
from persona.persona import Persona
from maze import Maze
from persona.cognitive_modules.plan import generate_wake_up_hour, generate_first_daily_plan, generate_hourly_schedule

def create_personas(sim_folder, start_time, maze):
    personas = {}
    personas_tile = {}

    init_env_file = f"{sim_folder}/environment/0.json"
    init_env = json.load(open(init_env_file))
    
    with open(f"{sim_folder}/reverie/meta.json") as json_file:  
        reverie_meta = json.load(json_file)

    for persona_name in reverie_meta['persona_names']:
        persona_folder = f"{sim_folder}/personas/{persona_name}"
        p_x = init_env[persona_name]["x"]
        p_y = init_env[persona_name]["y"]
        curr_persona = Persona(persona_name, persona_folder)

        # Initialize curr_time for the persona
        curr_persona.scratch.curr_time = start_time

        personas[persona_name] = curr_persona
        personas_tile[persona_name] = (p_x, p_y)
        maze.tiles[p_y][p_x]["events"].add(curr_persona.scratch.get_curr_event_and_desc())

    return personas, personas_tile

def _long_term_planning(persona, new_day):
    """
    Formulates the persona's daily long-term plan if it is the start of a new 
    day. This basically has two components: first, we create the wake-up hour, 
    and second, we create the hourly schedule based on it. 
    """
    # We start by creating the wake up hour for the persona. 
    wake_up_hour = generate_wake_up_hour(persona)

    # When it is a new day, we start by creating the daily_req of the persona.
    if new_day == "First day": 
        # Bootstrapping the daily plan for the start of then generation:
        persona.scratch.daily_req = generate_first_daily_plan(persona, 
                                                              wake_up_hour)
    elif new_day == "New day":
        # TODO: Implement revise_identity(persona) if needed
        persona.scratch.daily_req = persona.scratch.daily_req

    # Based on the daily_req, we create an hourly schedule for the persona, 
    # which is a list of todo items with a time duration (in minutes) that 
    # add up to 24 hours.
    persona.scratch.f_daily_schedule = generate_hourly_schedule(persona, 
                                                                wake_up_hour)
    persona.scratch.f_daily_schedule_hourly_org = (persona.scratch
                                                   .f_daily_schedule[:])

def populate_schedules(personas, maze, start_time):
    for persona_name, persona in personas.items():
        new_day = "First day" if persona.scratch.curr_time.day == start_time.day else "New day"
        _long_term_planning(persona, new_day)

# Usage example
if __name__ == "__main__":
    sim_folder = "../../environment/frontend_server/storage/simulation-test"
    start_time = datetime.datetime.strptime("June 25, 2022, 00:00:00", "%B %d, %Y, %H:%M:%S")
    maze = Maze("your_maze_name")

    personas, personas_tile = create_personas(sim_folder, start_time, maze)
    populate_schedules(personas, maze, start_time)

    # Now you can access and test the personas and their schedules
    for persona_name, persona in personas.items():
        print(f"Persona: {persona_name}")
        print(f"Schedule: {persona.scratch.f_daily_schedule}")
        print("---")