import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import init_embeddings
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


resume_folder = "E:\SUNBEAM_INTERN\Fake_resumes"

pdf_files = [
    os.path.join(resume_folder, f)
    for f in os.listdir(resume_folder)
    if f.lower().endswith(".pdf")

]

for pdf_file in pdf_files:
    file_name = os.path.basename(pdf_file)
    resme_id = os.path.splitext(file_name)[0]
    print(resme_id)


