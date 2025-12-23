from langchain_text_splitters import RecursiveCharacterTextSplitter

code_splitter = RecursiveCharacterTextSplitter.from_language(language = 'python',
                                chunk_size = 500, chunk_overlap = 100)

with open("dummy_code.py", 'r') as file:
    raw_text = file.read()

# print("Raw Text: ", raw_text)
docs = code_splitter.create_documents([raw_text])


print(docs[0])
print("\n\n")
print(docs[1])
print("\n\n")
print(docs[2])