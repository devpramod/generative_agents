import json
import datetime
import random
from persona.persona import Persona
from openai import OpenAI
from maze import Maze
from persona.cognitive_modules.plan import generate_wake_up_hour, generate_first_daily_plan, generate_hourly_schedule

client = OpenAI()

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


def GPT_request(prompt, gpt_parameter): 
  """
  Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
  server and returns the response. 
  ARGS:
    prompt: a str prompt
    gpt_parameter: a python dictionary with the keys indicating the names of  
                   the parameter and the values indicating the parameter 
                   values.   
  RETURNS: 
    a str of GPT-3's response. 
  """
  try: 
    messages = [{
      "role": "system", "content": prompt
    }]
    response = client.chat.completions.create(
                model=gpt_parameter["engine"],
                messages=messages,
                temperature=gpt_parameter["temperature"],
                max_tokens=gpt_parameter["max_tokens"],
                top_p=gpt_parameter["top_p"],
                frequency_penalty=gpt_parameter["frequency_penalty"],
                presence_penalty=gpt_parameter["presence_penalty"],
                stream=gpt_parameter["stream"],
                stop=gpt_parameter["stop"],)

    return response.choices[0].message.content
  except Exception as e:
    print(f"Error: {e}")
    return "TOKEN LIMIT EXCEEDED"

prompt_triple_action = """
Task: Turn the input into (subject, predicate, object). 

Input: Sam Johnson is eating breakfast. 
Output: (Sam Johnson, eat, breakfast) 
--- 
Input: Joon Park is brewing coffee.
Output: (Joon Park, brew, coffee)
---
Input: Jane Cook is sleeping. 
Output: (Jane Cook, is, sleep)
---
Input: Michael Bernstein is writing email on a computer. 
Output: (Michael Bernstein, write, email)
---
Input: Percy Liang is teaching students in a classroom. 
Output: (Percy Liang, teach, students)
---
Input: Merrie Morris is running on a treadmill. 
Output: (Merrie Morris, run, treadmill)
---
Input: Isabella Rodriguez is sleeping. 
Output: (Isabella Rodriguez,
"""
prompt_triple_action_v2 = f"""Task: Convert the given action into a triple format (subject, predicate, object).
Rules:
1. Subject is always the person's full name.
2. Predicate is the main verb in base form, or "is" for states of being.
3. Object is what the action is done to, or the base form of a state verb.
4. Always maintain the order: (subject, predicate, object)
5. Only provide the predicate and object, as the subject will be given.

Examples:
Input: Sam Johnson is eating breakfast.
Output: (Sam Johnson, eat, breakfast)

Input: Jane Cook is sleeping.
Output: (Jane Cook, is, sleep)

Input: Michael Bernstein is writing email on a computer.
Output: (Michael Bernstein, write, email)

Now, convert the following action:
Input: Isabella Rodriguez is sleeping.
Output: (Isabella Rodriguez, """

if __name__ == "__main__":
  # print (ChatGPT_request(prompt_triple_action))
  
# below functions are for prompt triple action
###################################################################################
  def __func_clean_up(gpt_response, prompt=""):
      cr = gpt_response.strip()
      cr = [i.strip() for i in cr.split(")")[0].split(",")]
      return cr

  # def __func_validate(gpt_response, prompt=""): 
  #   try: 
  #     gpt_response = __func_clean_up(gpt_response, prompt="")
  #     if len(gpt_response) != 2: 
  #       return False
  #   except: return False
  #   return True
  
  def __func_validate(response, action, persona):
    name = persona.Name
    # Check if the response is in the correct format
    if not (response.startswith('Isabella Rodriguez, ') and response.endswith(')')):
        return False
    
    components = response[:-1].split(', ')[1:]  # Remove closing parenthesis and split
    if len(components) != 2:
        return False
    
    predicate, obj = components
    
    # Check if the predicate is a valid verb form
    if predicate not in ['is', 'are'] and not predicate.isalpha():
        return False
    
    # Check if the object is present in the original action or is a base verb form
    if obj not in action and not obj.isalpha():
        return False
    
    return True

  gpt_param = {"engine": "gpt-4o", "max_tokens": 30, 
               "temperature": 0, "top_p": 1, "stream": False,
               "frequency_penalty": 0, "presence_penalty": 0, "stop": ["\n"]}

  print(GPT_request(prompt_triple_action, gpt_param))

  

#   verbose = True
#   final = ""
#   # breakpoint()
#   for i in range(5): 
#       curr_gpt_response = GPT_request(prompt_triple_action, gpt_param)
#       try:
#         if __func_validate(curr_gpt_response, "Isabella Rodriguez is sleeping."): 
#           print(__func_clean_up(curr_gpt_response))
#           break
#         if verbose: 
#           print ("---- repeat count: ", i, curr_gpt_response)
#           print (curr_gpt_response)
#           print ("~~~~")
#       except:
#         pass
###########################################################################################    