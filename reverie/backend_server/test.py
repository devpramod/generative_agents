"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: gpt_structure.py
Description: Wrapper functions for calling OpenAI APIs.
"""
import json
import random
# import openai
from openai import OpenAI
import time 

from utils import *
# openai.api_key = openai_api_key

# openai_api_key = "EMPTY"
# openai_api_base = "http://0.0.0.0:8000/v1"

client = OpenAI()

def ChatGPT_request(prompt): 
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
  # temp_sleep()
  try: 
    completion = client.chat.completions.create(
    model="gpt-4o", 
    messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content
  
  except Exception as e: 
    print ("ChatGPT ERROR")
    print(e)
    return "ChatGPT ERROR"

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


prompt = """
---
Character 1: Maria Lopez is working on her physics degree and streaming games on Twitch to make some extra money. She visits Hobbs Cafe for studying and eating just about everyday.
Character 2: Klaus Mueller is writing a research paper on the effects of gentrification in low-income communities.

Past Context: 
138 minutes ago, Maria Lopez and Klaus Mueller were already conversing about Maria's research paper mentioned by Klaus This context takes place after that conversation.

Current Context: Maria Lopez was attending her Physics class (preparing for the next lecture) when Maria Lopez saw Klaus Mueller in the middle of working on his research paper at the library (writing the introduction).
Maria Lopez is thinking of initating a conversation with Klaus Mueller.
Current Location: library in Oak Hill College

(This is what is in Maria Lopez's head: Maria Lopez should remember to follow up with Klaus Mueller about his thoughts on her research paper. Beyond this, Maria Lopez doesn't necessarily know anything more about Klaus Mueller) 

(This is what is in Klaus Mueller's head: Klaus Mueller should remember to ask Maria Lopez about her research paper, as she found it interesting that he mentioned it. Beyond this, Klaus Mueller doesn't necessarily know anything more about Maria Lopez) 

Here is their conversation. 

Maria Lopez: "
---
Output the response to the prompt above in json. The output should be a list of list where the inner lists are in the form of ["<Name>", "<Utterance>"]. Output multiple utterances in ther conversation until the conversation comes to a natural conclusion.
Example output json:
{"output": "[["Jane Doe", "Hi!"], ["John Doe", "Hello there!"] ... ]"}
"""



prompt_main_room_err = """
Jane Anderson is in kitchen in Jane Anderson's house.
Jane Anderson is going to Jane Anderson's house that has the following areas: {kitchen,  bedroom, bathroom}
Stay in the current area if the activity can be done there. Never go into other people's rooms unless necessary.
For cooking, Jane Anderson should go to the following area in Jane Anderson's house:
Answer: {kitchen}
---
Tom Watson is in common room in Tom Watson's apartment. 
Tom Watson is going to Hobbs Cafe that has the following areas: {cafe}
Stay in the current area if the activity can be done there. Never go into other people's rooms unless necessary.
For getting coffee, Tom Watson should go to the following area in Hobbs Cafe:
Answer: {cafe}
---
Isabella Rodriguez is going to Isabella Rodriguez's apartment that has the following areas: {main room}\n
* Stay in the current area if the activity can be done there. \n
* NEVER go into other people's rooms unless necessary.\n
Isabella Rodriguez is [Monday February 13 -- 00:00 AM] Activity: Isabella is sleeping. For [Monday February 13 -- 00:00 AM] Activity: Isabella is sleeping, Isabella Rodriguez should go to the following area in Isabella Rodriguez's apartment (MUST pick one of {main room}):\n

Answer: {
"""

prompt_task_scheduling_err = """
Describe subtasks in 5 min increments. 
---
Name: Kelly Bronson
Age: 35
Backstory: Kelly always wanted to be a teacher, and now she teaches kindergarten. During the week, she dedicates herself to her students, but on the weekends, she likes to try out new restaurants and hang out with friends. She is very warm and friendly, and loves caring for others.
Personality: sweet, gentle, meticulous
Location: Kelly is in an older condo that has the following areas: {kitchen, bedroom, dining, porch, office, bathroom, living room, hallway}.
Currently: Kelly is a teacher during the school year. She teaches at the school but works on lesson plans at home. She is currently living alone in a single bedroom condo.
Daily plan requirement: Kelly is planning to teach during the morning and work from home in the afternoon.s

Today is Saturday May 10. From 08:00am ~09:00am, Kelly is planning on having breakfast, from 09:00am ~ 12:00pm, Kelly is planning on working on the next day's kindergarten lesson plan, and from 12:00 ~ 13pm, Kelly is planning on taking a break. 
In 5 min increments, list the subtasks Kelly does when Kelly is working on the next day's kindergarten lesson plan from 09:00am ~ 12:00pm (total duration in minutes: 180):
1) Kelly is reviewing the kindergarten curriculum standards. (duration in minutes: 15, minutes left: 165)
2) Kelly is brainstorming ideas for the lesson. (duration in minutes: 30, minutes left: 135)
3) Kelly is creating the lesson plan. (duration in minutes: 30, minutes left: 105)
4) Kelly is creating materials for the lesson. (duration in minutes: 30, minutes left: 75)
5) Kelly is taking a break. (duration in minutes: 15, minutes left: 60)
6) Kelly is reviewing the lesson plan. (duration in minutes: 30, minutes left: 30)
7) Kelly is making final changes to the lesson plan. (duration in minutes: 15, minutes left: 15)
8) Kelly is printing the lesson plan. (duration in minutes: 10, minutes left: 5)
9) Kelly is putting the lesson plan in her bag. (duration in minutes: 5, minutes left: 0)
---
Name: Isabella Rodriguez
Age: 34
Innate traits: friendly, outgoing, hospitable
Learned traits: Isabella Rodriguez is a cafe owner of Hobbs Cafe who loves to make people feel welcome. She is always looking for ways to make the cafe a place where people can come to relax and enjoy themselves.
Currently: Isabella Rodriguez is planning on having a Valentine's Day party at Hobbs Cafe with her customers on February 14th, 2023 at 5pm. She is gathering party material, and is telling everyone to join the party at Hobbs Cafe on February 14th, 2023, from 5pm to 7pm.
Lifestyle: Isabella Rodriguez goes to bed around 11pm, awakes up around 6am.
Daily plan requirement: Isabella Rodriguez opens Hobbs Cafe at 8am everyday, and works at the counter until 8pm, at which point she closes the cafe.
Current Date: Monday February 13

Today is February 13, 2023. From 00:00AM ~ 08:00AM, Isabella Rodriguez is planning on sleeping, 08:00AM ~ 09:00AM, Isabella Rodriguez is planning on [(ID:E81HYW) Monday February 13 -- 08:00 AM] Activity: Isabella is waking up and completing her morning routine, 09:00AM ~ 10:00AM, Isabella Rodriguez is planning on [Monday February 13 -- 09:00 AM] Activity: Isabella is opening Hobbs Cafe and setting up for the day.
In 5 min increments, list the subtasks Isabella does when Isabella is [(ID:E81HYW) Monday February 13 -- 08:00 AM] Activity: Isabella is waking up and completing her morning routine from 08:00AM ~ 09:00AM (total duration in minutes 60): 
1) Isabella is
"""


# below functions are for prompt triple action
def __func_clean_up(gpt_response, prompt=""):
    cr = gpt_response.strip()
    cr = [i.strip() for i in cr.split(")")[0].split(",")]
    return cr

def __func_validate(gpt_response, prompt=""): 
  try: 
    gpt_response = __func_clean_up(gpt_response, prompt="")
    if len(gpt_response) != 2: 
      return False
  except: return False
  return True 


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

prompt_act_obj_desc = """
Task: We want to understand the state of an object that is being used by someone. 

Let's think step by step. 
We want to know about bed's state. 
Step 1. Isabella Rodriguez is at/using the sleeping.
Step 2. Describe the bed's state: bed is

Output the response to the prompt above in json. The output should ONLY contain the phrase that should go in <fill in>.
Example output json:
{"output": "being fixed"}
"""

if __name__ == "__main__":
  print (ChatGPT_request(prompt_act_obj_desc))

  #gpt_param = {"engine": "gpt-4o", "max_tokens": 30, 
              #  "temperature": 0, "top_p": 1, "stream": False,
              #  "frequency_penalty": 0, "presence_penalty": 0, "stop": ["\n"]}
  

  #curr_gpt_response = GPT_request(prompt_triple_action, gpt_param)

  
