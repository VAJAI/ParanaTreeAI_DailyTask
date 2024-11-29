from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage,HumanMessage
from langchain.schema.output_parser import StrOutputParser
import uvicorn
import os

load_dotenv()

app = FastAPI()
key =os.getenv("OPENAI_API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class text(BaseModel):
    message:str
    
class query(BaseModel):
    query: str

@app.post('/chatmodel')
async def openai(request : text):
    text = request.message
    model=ChatOpenAI(api_key=key,model='gpt-4-0613',temperature=1,max_tokens=200)
    
    messages=[SystemMessage(content="Complete the sentence"),
             HumanMessage(content=text)]
    result=model.invoke(messages)
    return result.content

@app.post('/faq')
async def faq_ans(request : query):
    query =request.query
    model = ChatOpenAI(model="gpt-4-0613",temperature=0)
    prompt_templete =ChatPromptTemplate.from_messages([
       ("system", "Don't answer irrelevent question from the context if asked them respond IRRELEVENT"),
            ("system",'''Q: What is LangChain?
                A: LangChain is a framework designed to simplify the process of building applications that utilize language models.
                Q: How do I set up my environment?
                A: Follow the instructions in the "Getting Started" section above. Ensure you have Python 3.10 or 3.11 installed, install Poetry, clone the repository, install dependencies, rename the .env.example file to .env, and activate the Poetry shell.
                Q: I am getting an error when running the examples. What should I do?
                A: Ensure all dependencies are installed correctly and your environment variables are set up properly. If the issue persists, seek help in the Skool community or open an issue on GitHub.
                Q: Can I contribute to this repository?
                A: Yes! Contributions are welcome. Please open an issue or submit a pull request with your changes.
                Q: Where can I find more information about LangChain?
                A: Check out the official LangChain documentation and join the Skool community for additional resources and support.
            '''),
            ("human","{content}")
    ])
    
    
    chain= prompt_templete | model | StrOutputParser()
    
    result =chain.invoke({"content":query})
    return result

# if __name__ == "__main__":
#     uvicorn.run(app,host='localhost',port=8080)