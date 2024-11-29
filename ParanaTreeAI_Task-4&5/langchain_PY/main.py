import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.schema import SystemMessage,HumanMessage
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

load_dotenv()

app = FastAPI()

class text(BaseModel):
    message: str

class query(BaseModel):
    query: str

key = os.getenv('OPENAI_API_KEY')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace "*" with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/chatmodel')
async def openai(request : text):
    text = request.message
    model = ChatOpenAI(api_key = key,model = 'gpt-4-0613',max_tokens = 200,temperature =1)

    messages = [SystemMessage(content="Complete the sentences"),
            HumanMessage(content=text)]

    result = model.invoke(messages)

    return result.content

@app.post('/FAQ')
async def faq(request : query):
    query = request.query
    model = ChatOpenAI(model="gpt-4-0613",temperature = 0)
    # Define prompt templates
    prompt_template = ChatPromptTemplate.from_messages(
        [
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
        ]
    )
    # Create the combined chain using LangChain Expression Language (LCEL)
    chain = prompt_template | model | StrOutputParser()

    # Run the chain
    result = chain.invoke({"content":query})
    return result


if __name__ == "__main__":
    uvicorn.run(app,host='localhost',port=8080)