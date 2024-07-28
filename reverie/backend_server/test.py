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


if __name__ == "__main__":
  print (ChatGPT_request(prompt_task_scheduling_err))
  