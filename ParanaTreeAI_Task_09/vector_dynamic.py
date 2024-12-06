from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore


from dotenv import load_dotenv
load_dotenv()
import os
pinecone_api_key = os.getenv("PINECONE_API_KEY")
openai_api_key=os.getenv("OPENAI_API_KEY")

## lets read the document
def read_doc(directory):
    file_loders=PyPDFDirectoryLoader(directory)
    documents=file_loders.load()
    return documents

doc=read_doc('documents/')
doc

## divide the doc the chunks
def chunk_data(docs,chunk_size=800,chunk_overlap=50):
    text_spiliters=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    doc=text_spiliters.split_documents(docs)
    return doc

document=chunk_data(docs=doc)
document

## embedding techniques of OPENAI
embeddings=OpenAIEmbeddings(api_key=openai_api_key)
embeddings

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
pc=Pinecone(api_key=pinecone_api_key)
index=pc.Index("vectorlangchain")
vector_store = PineconeVectorStore.from_documents(
    documents=document,
    embedding=embeddings,
    index_name="vectorlangchain"
)


query = "What the data about technical skills in this document?"
retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k":3,'score_threshold': 0.8}
    )

relevent_doc=retriever.invoke(query)

for i,doc in enumerate(relevent_doc,1):
    print(f"Document {i}:\n {doc.page_content}\n")
    print(f"Source: {doc.metadata['source']}\n")
    

stats = index.describe_index_stats()
print("Index Stats:", stats)
