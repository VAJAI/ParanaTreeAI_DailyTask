from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from secret import OPENAI_API_KEY
import os

load_dotenv()

os.environ['OPENAI_API_KEY']= OPENAI_API_KEY
llm=ChatOpenAI(temperature=0.5)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],   
)

class Question(BaseModel):
    text:str

@app.post('/ask')
async def lang_api(question:Question):
    try:
        faq={
            "what is the langchain": "LangChain is a framework for building applications powered by language models.", 
            
            "who is the ceo of google": "Sundar Pichai is the CEO of Google.",
            
            "what is python": "Python is a versatile programming language.",
            
            "what is artificial intelligence": "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and learn like humans."}
        
        # prompt_templete = ChatPromptTemplate.from_messages([
        #     ("system","Your the assistant to answer my question"),
        #     ("user","{question}")])
        
        question_text =question.text.lower()
        
        if question_text in faq:
            return {"Answer":faq[question_text]}
        else:
            # response=prompt_templete.format(question=question.text)
            response=f"Your are a help full assitant {question}"
            llm_response=llm.invoke(response)
            return {"Answer":llm_response.content}
        
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
   
