import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import init_embeddings


embed_model = init_embeddings(
    model= "text-embedding-nomic-embed-text-v1",
    provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "not-needed",
    check_embedding_ctx_length = False
)


# db = chromadb.Client(settings = chromadb.Settings(persistent_directory = "./knowledge_base"))
# collection = db.get_or_create_collection("resumes")

# collection.add(ids = ["resume_id"], embeddings = [], metadatas = [], documents = [])
# db.persist()





def load_pdf_resume(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    resume_content = ""

    for page in docs:
        resume_content += page.page_content

    metadata = {
        "source": pdf_path,
        "page_count": len(docs)
    }

    return resume_content, metadata



resume_path = "E:/SUNBEAM_INTERN/Fake_resumes/resume-003.pdf"

resume_text, resume_info = load_pdf_resume(resume_path)

# print("Resume_info : ", resume_info)
# print("Resume_text: ", resume_text)



resume_embeddings = embed_model.embed_documents([resume_text])
# print("len embeddings = ", len(resume_embeddings))
for embedding in resume_embeddings:
    print(f"Len : {len(embedding)} ----> {embedding[:5]}")




db = chromadb.PersistentClient(path = "./knowledge_base")
collection = db.get_or_create_collection("resumes")

# collection.delete(ids=["resume-003"])


# collection.add(ids = ["resume-003"], embeddings =resume_embeddings, metadatas = [resume_info], documents = [resume_text])


all_data = collection.get()

print("All Data: ", all_data)

print("Total records:", collection.count())
