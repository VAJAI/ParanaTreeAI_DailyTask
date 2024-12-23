from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import openai
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key=os.getenv("OPENAI_API_KEY")

model=ChatOpenAI(api_key=openai_api_key,temperature=0.5)

Text="I want a luxurious hotel near the Eiffel Tower."
model=ChatOpenAI(temperature=0.4,api_key=openai_api_key)
prompt_templete_name=ChatPromptTemplate.from_messages([
("system", "You are a helpful AI assistant specializing in restaurant-related queries."
"Answer only questions related to restaurants and Hotels. If the question is irrelevant or about other topics, ""respond with 'Irrelevant'."),
("human", "List out the best restaurants in {text}")
])
chain =  prompt_templete_name | model | StrOutputParser()
hotel_result= chain.invoke({"text":Text})
# print(hotel_result)

# Example: Retain multi-turn context
context = "User asked for 5-star hotels in Paris."
new_query = "Also, show me budget hotels." 

full_context = context + " " + new_query

response=openai.chat.completions.create(
    model="gpt-4",
    messages=(
        {"role":"system","content":"your a helpful AI assistant"},
        {"role":"user","content":full_context}
        )
)
print(response.choices[0].message.content)
