import json
import datetime
import random
from persona.persona import Persona
from maze import Maze
from persona.cognitive_modules.plan import generate_wake_up_hour, generate_first_daily_plan, generate_hourly_schedule

# def create_personas(sim_folder, start_time, maze):
#     personas = {}
#     personas_tile = {}

#     init_env_file = f"{sim_folder}/environment/0.json"
#     init_env = json.load(open(init_env_file))
    
#     with open(f"{sim_folder}/reverie/meta.json") as json_file:  
#         reverie_meta = json.load(json_file)

#     for persona_name in reverie_meta['persona_names']:
#         persona_folder = f"{sim_folder}/personas/{persona_name}"
#         p_x = init_env[persona_name]["x"]
#         p_y = init_env[persona_name]["y"]
#         curr_persona = Persona(persona_name, persona_folder)

#         # Initialize curr_time for the persona
#         curr_persona.scratch.curr_time = start_time

#         personas[persona_name] = curr_persona
#         personas_tile[persona_name] = (p_x, p_y)
#         maze.tiles[p_y][p_x]["events"].add(curr_persona.scratch.get_curr_event_and_desc())

#     return personas, personas_tile

def create_persona(sim_folder, start_time, maze, persona_name):
    init_env_file = f"{sim_folder}/environment/0.json"
    init_env = json.load(open(init_env_file))
    
    with open(f"{sim_folder}/reverie/meta.json") as json_file:  
        reverie_meta = json.load(json_file)

    if persona_name in reverie_meta['persona_names']:
        persona_folder = f"{sim_folder}/personas/{persona_name}"
        p_x = init_env[persona_name]["x"]
        p_y = init_env[persona_name]["y"]
        curr_persona = Persona(persona_name, persona_folder)

        # Initialize curr_time for the persona
        curr_persona.scratch.curr_time = start_time

        maze.tiles[p_y][p_x]["events"].add(curr_persona.scratch.get_curr_event_and_desc())
        return curr_persona, (p_x, p_y)
    else:
        print(f"Persona '{persona_name}' not found in the simulation metadata.")
        return None, None

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

# def populate_schedules(personas, maze, start_time):
#     for persona_name, persona in personas.items():
#         new_day = "First day" if persona.scratch.curr_time.day == start_time.day else "New day"
#         _long_term_planning(persona, new_day)

def populate_schedules(persona, maze, start_time):
    if persona:
        new_day = "First day" if persona.scratch.curr_time.day == start_time.day else "New day"
        _long_term_planning(persona, new_day)

# def create_prompt_input(persona, task, duration, test_input=None):

#     """
#     Today is Saturday June 25. From 00:00 ~ 06:00am, Maeve is 
#     planning on sleeping, 06:00 ~ 07:00am, Maeve is 
#     planning on waking up and doing her morning routine, 
#     and from 07:00am ~08:00am, Maeve is planning on having breakfast.  
#     """
      
#     curr_f_org_index = persona.scratch.get_f_daily_schedule_hourly_org_index()
#     all_indices = []
#     # if curr_f_org_index > 0: 
#     #   all_indices += [curr_f_org_index-1]
#     all_indices += [curr_f_org_index]
#     if curr_f_org_index+1 <= len(persona.scratch.f_daily_schedule_hourly_org): 
#       all_indices += [curr_f_org_index+1]
#     if curr_f_org_index+2 <= len(persona.scratch.f_daily_schedule_hourly_org): 
#       all_indices += [curr_f_org_index+2]

#     curr_time_range = ""

#     print ("DEBUG")
#     print (persona.scratch.f_daily_schedule_hourly_org)
#     print (all_indices)

#     summ_str = f'Today is {persona.scratch.curr_time.strftime("%B %d, %Y")}. '
#     summ_str += f'From '
#     for index in all_indices: 
#       print ("index", index)
#       if index < len(persona.scratch.f_daily_schedule_hourly_org): 
#         start_min = 0
#         for i in range(index): 
#           start_min += persona.scratch.f_daily_schedule_hourly_org[i][1]
#         end_min = start_min + persona.scratch.f_daily_schedule_hourly_org[index][1]
#         start_time = (datetime.datetime.strptime("00:00:00", "%H:%M:%S") 
#                       + datetime.timedelta(minutes=start_min)) 
#         end_time = (datetime.datetime.strptime("00:00:00", "%H:%M:%S") 
#                       + datetime.timedelta(minutes=end_min)) 
#         start_time_str = start_time.strftime("%H:%M%p")
#         end_time_str = end_time.strftime("%H:%M%p")
#         summ_str += f"{start_time_str} ~ {end_time_str}, {persona.name} is planning on {persona.scratch.f_daily_schedule_hourly_org[index][0]}, "
#         if curr_f_org_index+1 == index:
#           curr_time_range = f'{start_time_str} ~ {end_time_str}'
#     summ_str = summ_str[:-2] + "."

#     prompt_input = []
#     prompt_input += [persona.scratch.get_str_iss()]
#     prompt_input += [summ_str]
#     # prompt_input += [persona.scratch.get_str_curr_date_str()]
#     prompt_input += [persona.scratch.get_str_firstname()]
#     prompt_input += [persona.scratch.get_str_firstname()]
#     prompt_input += [task]
#     prompt_input += [curr_time_range]
#     prompt_input += [duration]
#     prompt_input += [persona.scratch.get_str_firstname()]
#     return prompt_input

import re

# def create_prompt_input(persona, task, duration, test_input=None):
#     curr_f_org_index = persona.scratch.get_f_daily_schedule_hourly_org_index()
#     all_indices = [curr_f_org_index]
#     if curr_f_org_index+1 < len(persona.scratch.f_daily_schedule_hourly_org): 
#         all_indices += [curr_f_org_index+1]
#     if curr_f_org_index+2 < len(persona.scratch.f_daily_schedule_hourly_org): 
#         all_indices += [curr_f_org_index+2]

#     curr_time_range = ""

#     summ_str = f'Today is {persona.scratch.curr_time.strftime("%B %d, %Y")}. '
#     summ_str += f'From '
#     for index in all_indices: 
#         if index < len(persona.scratch.f_daily_schedule_hourly_org): 
#             start_min = sum(persona.scratch.f_daily_schedule_hourly_org[i][1] for i in range(index))
#             end_min = start_min + persona.scratch.f_daily_schedule_hourly_org[index][1]
#             start_time = (datetime.datetime.strptime("00:00:00", "%H:%M:%S") 
#                           + datetime.timedelta(minutes=start_min)) 
#             end_time = (datetime.datetime.strptime("00:00:00", "%H:%M:%S") 
#                           + datetime.timedelta(minutes=end_min)) 
#             start_time_str = start_time.strftime("%H:%M%p")
#             end_time_str = end_time.strftime("%H:%M%p")
#             activity = persona.scratch.f_daily_schedule_hourly_org[index][0]
#             # Extract only the activity description
#             activity = re.sub(r'\[.*?\]\s*', '', activity)
#             activity = re.sub(r'.*?Activity:\s*', '', activity)
#             summ_str += f"{start_time_str} ~ {end_time_str}, {persona.name} is planning on {activity}, "
#             if curr_f_org_index == index:
#                 curr_time_range = f'{start_time_str} ~ {end_time_str}'
#     summ_str = summ_str[:-2] + "."

#     prompt_input = []
#     prompt_input += [persona.scratch.get_str_iss()]
#     prompt_input += [summ_str]
#     prompt_input += [persona.scratch.get_str_firstname()]
#     prompt_input += [persona.scratch.get_str_firstname()]

#     # Extract only the activity description from the task
#     task = re.sub(r'\[.*?\]\s*', '', task)
#     task = re.sub(r'.*?Activity:\s*', '', task)

#     prompt_input += [task]
#     prompt_input += [curr_time_range]
#     prompt_input += [duration]
#     prompt_input += [persona.scratch.get_str_firstname()]
#     return prompt_input

# def create_prompt_input(persona, task, duration, test_input=None):
#     curr_f_org_index = persona.scratch.get_f_daily_schedule_hourly_org_index()
#     all_indices = [curr_f_org_index]
#     if curr_f_org_index+1 < len(persona.scratch.f_daily_schedule_hourly_org): 
#         all_indices += [curr_f_org_index+1]
#     if curr_f_org_index+2 < len(persona.scratch.f_daily_schedule_hourly_org): 
#         all_indices += [curr_f_org_index+2]

#     curr_time_range = ""

#     summ_str = f'Today is {persona.scratch.curr_time.strftime("%B %d, %Y")}. '
#     summ_str += f'From '
#     for index in all_indices: 
#         if index < len(persona.scratch.f_daily_schedule_hourly_org): 
#             start_min = sum(persona.scratch.f_daily_schedule_hourly_org[i][1] for i in range(index))
#             end_min = start_min + persona.scratch.f_daily_schedule_hourly_org[index][1]
#             start_time = (datetime.datetime.strptime("00:00:00", "%H:%M:%S") 
#                           + datetime.timedelta(minutes=start_min)) 
#             end_time = (datetime.datetime.strptime("00:00:00", "%H:%M:%S") 
#                           + datetime.timedelta(minutes=end_min)) 
#             start_time_str = start_time.strftime("%H:%M%p")
#             end_time_str = end_time.strftime("%H:%M%p")
#             activity = persona.scratch.f_daily_schedule_hourly_org[index][0]
#             # Extract only the activity description
#             activity = re.sub(r'\[.*?\]\s*', '', activity)
#             activity = re.sub(r'.*?Activity:\s*', '', activity)
#             summ_str += f"{start_time_str} ~ {end_time_str}, {persona.name} is planning on {activity}, "
#             if curr_f_org_index == index:
#                 curr_time_range = f'{start_time_str} ~ {end_time_str}'
#     summ_str = summ_str[:-2] + "."

#     prompt_input = []
#     prompt_input += [persona.scratch.get_str_iss()]
#     prompt_input += [summ_str]
#     prompt_input += [persona.scratch.get_str_firstname()]
#     prompt_input += [persona.scratch.get_str_firstname()]

#     # Extract only the activity description from the task
#     task = re.sub(r'\[.*?\]\s*', '', task)
#     task = re.sub(r'.*?Activity:\s*', '', task)

#     prompt_input += [task]
#     prompt_input += [curr_time_range]
#     prompt_input += [duration]
#     prompt_input += [persona.scratch.get_str_firstname()]
#     return prompt_input

# def create_prompt_input(persona, task, duration, test_input=None):
#     curr_f_org_index = persona.scratch.get_f_daily_schedule_hourly_org_index()
#     all_indices = [curr_f_org_index]
#     if curr_f_org_index+1 < len(persona.scratch.f_daily_schedule_hourly_org): 
#         all_indices += [curr_f_org_index+1]
#     if curr_f_org_index+2 < len(persona.scratch.f_daily_schedule_hourly_org): 
#         all_indices += [curr_f_org_index+2]

#     curr_time_range = ""

#     summ_str = f'Today is {persona.scratch.curr_time.strftime("%B %d, %Y")}. '
#     for index in all_indices: 
#         if index < len(persona.scratch.f_daily_schedule_hourly_org): 
#             start_min = sum(persona.scratch.f_daily_schedule_hourly_org[i][1] for i in range(index))
#             end_min = start_min + persona.scratch.f_daily_schedule_hourly_org[index][1]
#             start_time = (datetime.datetime.strptime("00:00:00", "%H:%M:%S") 
#                           + datetime.timedelta(minutes=start_min)) 
#             end_time = (datetime.datetime.strptime("00:00:00", "%H:%M:%S") 
#                           + datetime.timedelta(minutes=end_min)) 
#             start_time_str = start_time.strftime("%I:%M %p")
#             end_time_str = end_time.strftime("%I:%M %p")
#             activity = persona.scratch.f_daily_schedule_hourly_org[index][0]
#             # Extract only the activity description
#             activity = re.sub(r'\[.*?\]\s*', '', activity)
#             activity = re.sub(r'.*?Activity:\s*', '', activity)
#             summ_str += f"From {start_time_str} to {end_time_str}, {persona.name} is planning on {activity}. "
#             if curr_f_org_index == index:
#                 curr_time_range = f'{start_time_str} to {end_time_str}'

#     prompt_input = []
#     prompt_input += [persona.scratch.get_str_iss()]
#     prompt_input += [summ_str]
#     prompt_input += [persona.scratch.get_str_firstname()]
#     prompt_input += [persona.scratch.get_str_firstname()]

#     # Extract only the activity description from the task
#     task = re.sub(r'\[.*?\]\s*', '', task)
#     task = re.sub(r'.*?Activity:\s*', '', task)

#     prompt_input += [task]
#     prompt_input += [curr_time_range]
#     prompt_input += [duration]
#     prompt_input += [persona.scratch.get_str_firstname()]
#     return prompt_input

def create_prompt_input(persona, task, duration, test_input=None):
    curr_f_org_index = persona.scratch.get_f_daily_schedule_hourly_org_index()
    all_indices = [curr_f_org_index]
    if curr_f_org_index+1 < len(persona.scratch.f_daily_schedule_hourly_org): 
        all_indices += [curr_f_org_index+1]
    if curr_f_org_index+2 < len(persona.scratch.f_daily_schedule_hourly_org): 
        all_indices += [curr_f_org_index+2]

    curr_time_range = ""

    summ_str = f'Today is {persona.scratch.curr_time.strftime("%B %d, %Y")}. '
    for index in all_indices: 
        if index < len(persona.scratch.f_daily_schedule_hourly_org): 
            start_min = sum(persona.scratch.f_daily_schedule_hourly_org[i][1] for i in range(index))
            end_min = start_min + persona.scratch.f_daily_schedule_hourly_org[index][1]
            start_time = (datetime.datetime.strptime("00:00:00", "%H:%M:%S") 
                          + datetime.timedelta(minutes=start_min)) 
            end_time = (datetime.datetime.strptime("00:00:00", "%H:%M:%S") 
                          + datetime.timedelta(minutes=end_min)) 
            start_time_str = start_time.strftime("%I:%M %p")
            end_time_str = end_time.strftime("%I:%M %p")
            activity = persona.scratch.f_daily_schedule_hourly_org[index][0]
            # Extract only the activity description
            activity = re.sub(r'\[.*?\]\s*', '', activity)
            activity = re.sub(r'.*?Activity:\s*', '', activity)
            summ_str += f"From {start_time_str} to {end_time_str}, {persona.name} is planning on {activity}. "
            if curr_f_org_index == index:
                curr_time_range = f'{start_time_str} to {end_time_str}'

    prompt_input = []
    prompt_input += [persona.scratch.get_str_iss()]
    prompt_input += [summ_str]
    prompt_input += [persona.scratch.get_str_firstname()]
    prompt_input += [persona.scratch.get_str_firstname()]

    # Extract only the activity description from the task
    task = re.sub(r'\[.*?\]\s*', '', task)
    task = re.sub(r'.*?Activity:\s*', '', task)

    prompt_input += [task]
    prompt_input += [curr_time_range]
    prompt_input += [str(duration)]
    prompt_input += [persona.scratch.get_str_firstname()]
    return prompt_input

def generate_prompt(curr_input, prompt_lib_file): 
  """
  Takes in the current input (e.g. comment that you want to classifiy) and 
  the path to a prompt file. The prompt file contains the raw str prompt that
  will be used, which contains the following substr: !<INPUT>! -- this 
  function replaces this substr with the actual curr_input to produce the 
  final promopt that will be sent to the GPT3 server. 
  ARGS:
    curr_input: the input we want to feed in (IF THERE ARE MORE THAN ONE
                INPUT, THIS CAN BE A LIST.)
    prompt_lib_file: the path to the promopt file. 
  RETURNS: 
    a str prompt that will be sent to OpenAI's GPT server.  
  """
  if type(curr_input) == type("string"): 
    curr_input = [curr_input]
  curr_input = [str(i) for i in curr_input]

  f = open(prompt_lib_file, "r")
  prompt = f.read()
  f.close()
  for count, i in enumerate(curr_input):   
    prompt = prompt.replace(f"!<INPUT {count}>!", i)
  if "<commentblockmarker>###</commentblockmarker>" in prompt: 
    prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
  return prompt.strip()


if __name__ == "__main__":
    sim_folder = "../../environment/frontend_server/storage/simulation-test"
    start_time = datetime.datetime.strptime("June 25, 2022, 00:00:00", "%B %d, %Y, %H:%M:%S")
    maze = Maze("your_maze_name")

    persona, persona_tile = create_persona(sim_folder, start_time, maze, "Isabella Rodriguez")
    populate_schedules(persona, maze, start_time)

    # access and test the personas and their schedules
    # for persona_name, persona in personas.items():
    #     print(f"Persona: {persona_name}")
    #     print(f"Schedule: {persona.scratch.f_daily_schedule}")
    #     print("---")
    # persona = personas['Isabella Rodriguez']

    prompt_template = "persona/prompt_template/v2/task_decomp_v3.txt"
    task = '[(ID:Q2rgHB) Saturday June 25 -- 08:00 AM] Activity: Isabella is waking up and completing her morning routine'
    duration = 60
    prompt_input = create_prompt_input(persona, task, duration)
    prompt = generate_prompt(prompt_input, prompt_template)
    breakpoint()