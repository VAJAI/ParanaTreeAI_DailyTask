import cohere_test 
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = ["Find a 5-star hotel in New York", "Luxury hotels in Manhattan"]

embeddings=model.encode(texts)
print(embeddings)


# from sklearn.metrics.pairwise import cosine_similarity

# similarity = cosine_similarity([embeddings[0]], [embeddings[1]])
# print(f"Cosine Similarity: {similarity[0][0]}")
# print("comparison complete")
