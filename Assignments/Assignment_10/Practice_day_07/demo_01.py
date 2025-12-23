from sentence_transformers import SentenceTransformer
import numpy as np


def cosine_similarity(a,b):
    return np.dot(a,b)/(np.linalg.norm(a)* np.linalg.norm(b))

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "I love football",
    "Soccer is my favourite sports",
    "Narendra Modi is Prime Minister of India"
]

embeddings = embed_model.encode(sentences)

print("Shape of embeddings: ", embeddings.shape)

for embed_vect in embeddings:
    print("Len: ", len(embed_vect), "---> ", embed_vect[:5])


print("Sentence 1 & 2 similarity: ", cosine_similarity(embeddings[0], embeddings[1]))
print("Sentence 2 & 3 similarity: ", cosine_similarity(embeddings[1], embeddings[2]))
