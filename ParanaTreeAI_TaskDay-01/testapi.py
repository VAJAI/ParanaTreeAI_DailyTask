from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
messages = [
    {"role":"system","content":"your the the AI Assitant"}
]
while True:
    user_msg= input("Enter your question")
    if user_msg !="":
        messages.append(
            {"role":"system","content":user_msg})
        
        response =client.chat.completions.create(
            model="chatgpt-4o-latest",
            messages=messages,
            temperature=0
            )
        
        bot_res =response.choices[0].message.content
        print("user_msg: ",user_msg)
        print("Assitant: ",bot_res)
        
        messages.append({
            "role":"Assitant","content":bot_res
        })
    
    else:
        print("Oops you dont continue the communication")
        break 