from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from pinecone import Pinecone
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain_pinecone import PineconeVectorStore

from dotenv import load_dotenv
import os

# Load API keys from .env file
load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")




# Read documents from a directory
def read_doc(directory):
    file_loaders = PyPDFDirectoryLoader(directory)
    documents = file_loaders.load()
    return documents

docs = read_doc('documents/')

# Split documents into chunks
def chunk_data(docs, chunk_size=800, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    doc_chunks = text_splitter.split_documents(docs)
    return doc_chunks

documents = chunk_data(docs=docs)

# Create embeddings
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Create a Pinecone index
index_name = "vectorlangchain" 

# Connect to Pinecone index
pc=Pinecone(api_key=pinecone_api_key)
index = pc.Index(index_name)
vector_store =PineconeVectorStore.from_documents(
    documents=documents,
    embedding=embeddings,
    index_name=index_name
)

# Create a retriever
retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 1, "score_threshold": 0.8}
)

# Add Conversation Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Define the Conversational Retrieval Chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=openai_api_key),
    retriever=retriever,
    memory=memory,
    verbose=True
)

# Simulated multi-turn conversation
print("Conversation Start")
response1 = qa_chain({"question": "What is the score of TCS iON NQT IT exam?"})
print("Bot:", response1['answer'])

response2 = qa_chain({"question": "Can you explain the exam details?"})
print("Bot:", response2['answer'])

response3 = qa_chain({"question": "What resources should I use to prepare?"})
print("Bot:", response3['answer'])

# Display the conversation history
print("\nConversation History:")
print(memory.load_memory_variables({})["chat_history"])
