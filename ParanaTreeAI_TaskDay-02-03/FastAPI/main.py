from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

load_dotenv()
openai.api_key=os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class Question(BaseModel):
    text: str
    
@app.post('/ask')
async def ask_api(question: Question):
    try:
        response=openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role":"user","content":question.text}],
            max_tokens=150,
            temperature=0.5,
        )
        assistant_message =response.choices[0].message.content
        return {"Answer":assistant_message.strip()}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
        
    
    
