import cohere
from dotenv import load_dotenv
import os

load_dotenv()

cohere_api_key=os.getenv("COHERE_API_KEY")

# Initialize Cohere client
co = cohere.Client(cohere_api_key)

# Input text
texts = ["Find a 5-star hotel in New York", "Luxury hotels in Manhattan"]

# Generate embeddings
response = co.embed(
    texts=texts,
    model="large"
)

embeddings = response.embeddings
print(embeddings)
