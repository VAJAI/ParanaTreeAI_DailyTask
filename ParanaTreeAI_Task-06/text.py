from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Example texts
texts = ["This is an example sentence.", "Another example for embeddings."]

# Generate embeddings
embeddings = model.encode(texts)

# Output
print("Embeddings shape:", embeddings.shape)  
print("First embedding vector:", embeddings[0])  


