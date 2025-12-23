from langchain_text_splitters import CharacterTextSplitter

text_splitter = CharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)

with open("dummy_data.txt", 'r') as file:
    raw_text = file.read()
 

docs = text_splitter.create_documents([raw_text])
print(docs[0],"\n\n")
print(docs[1])

