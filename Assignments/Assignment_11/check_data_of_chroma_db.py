import chromadb

db = chromadb.PersistentClient(path = "./knowledge_base")
collection = db.get_or_create_collection("resumes")


all_data = collection.get()
print("All data: ", all_data["metadatas"])


# print("Count of data in collection: ", collection.count())