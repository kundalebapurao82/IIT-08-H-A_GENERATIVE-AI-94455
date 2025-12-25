from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import init_embeddings
import chromadb
import os
from dotenv import load_dotenv
load_dotenv()


embed_model = init_embeddings(
    model= "text-embedding-nomic-embed-text-v1",
    provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "not-needed",
    check_embedding_ctx_length = False
)



resume_folder = os.getenv("RESUME_FOLDER")

# Load all pdf files....
pdf_files = [
    os.path.join(resume_folder, f)
    for f in os.listdir(resume_folder)
    if f.lower().endswith(".pdf")

]

# ============== initialize chromadb ==================

db = chromadb.PersistentClient(path = "./knowledge_base")
collection = db.get_or_create_collection("resumes")


def get_resume_id(file_path):
    file_name = os.path.basename(file_path)
    resume_id = os.path.splitext(file_name)[0]
    return resume_id

# =============== pdf loader ===========
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



# loop of each pdf file
for pdf_file_path in pdf_files:
    # get resume id
    resume_id = get_resume_id(pdf_file_path)

    # get content(text) and metadata

    resume_text, resume_info = load_pdf_resume(pdf_file_path)

    # managing empty pdf
    if not resume_text.strip():
        print(f"Empty text in {resume_id}, skipping")
        continue

    # get embedding for resume_text

    resume_embeddings = embed_model.embed_documents([resume_text])
    # print("len resume mbeddings: ",len(resume_embeddings))
    
    collection.add(
        ids = [resume_id], 
        embeddings = resume_embeddings, 
        metadatas = [resume_info], 
        documents = [resume_text]
    )
    

    







