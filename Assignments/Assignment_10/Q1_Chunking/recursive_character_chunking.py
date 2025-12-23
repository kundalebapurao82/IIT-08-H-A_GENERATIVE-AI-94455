from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 800, chunk_overlap = 200,
                                               separators = ["\n\n", "\n", " ", ""])

with open("dummy_data.txt",'r') as file:
    raw_data = file.read()

docs = text_splitter.create_documents([raw_data])

# for doc in docs:
#     print(doc.page_content)
#     print("\n\n")

print(docs[0])
print("\n\n")
print(docs[1])
print("\n\n")
print(docs[2])