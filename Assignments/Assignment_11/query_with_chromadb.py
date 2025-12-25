from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import init_embeddings
import chromadb
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize embed model
embed_model = init_embeddings(
    model= "text-embedding-nomic-embed-text-v1",
    provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "not-needed",
    check_embedding_ctx_length = False
)

# initialize chroma db
db = chromadb.PersistentClient(path = "./knowledge_base")
collection = db.get_or_create_collection("resumes")

# Get HR query
HR_query = input("HR Query: ")

# embed HR query
query_embedding = embed_model.embed_query(HR_query)

# similarity search
# get top 4 results with similarity to given query_embedding
results = collection.query( query_embeddings = [query_embedding], n_results = 4)

print("Results: ")
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print("Metadata: ", meta)
    print("Document : ",doc)









