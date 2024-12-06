from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

key=os.getenv("OPENAI_API_KEY")

# Initialize the memory and model
memory = ConversationBufferMemory(return_messages=True)  
chat_model = ChatOpenAI(model="gpt-4", temperature=0)

# Define a conversation chain
conversation = ConversationChain(
    llm=chat_model,
    memory=memory,
    verbose=True  # To print intermediate steps
)

# Start a conversation
response1 = conversation.run("Hi, can you tell me about the Great Wall of China?")
print("Bot:", response1)

response2 = conversation.run("How long is it?")
print("Bot:", response2)


