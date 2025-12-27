import streamlit as s
from langchain_community.document_loaders import PyPDFLoader
from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings
import chromadb
import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import json
load_dotenv()


qroq_api_key = os.getenv("GROQ_API_KEY")


if "view" not in s.session_state:
    s.session_state.view = "main"

if "embed_model" not in s.session_state:
    s.session_state.embed_model = None

if "collection" not in s.session_state:
    s.session_state.collection = None

if "filepath" not in s.session_state:
    s.session_state.filepath = None

if "update_id" not in s.session_state:
    s.session_state.update_id = None


# initialize chroma db
db = chromadb.PersistentClient(path = "./knowledge_base")
collection = db.get_or_create_collection("resumes")
# s.session_state.collection = collection

# Initialize embed model
embed_model = init_embeddings(
    model= "text-embedding-nomic-embed-text-v1",
    provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "not-needed",
    check_embedding_ctx_length = False
)
# s.session_state.embed_model = embed_model


# Initialize llm
llm = init_chat_model(
     model = "llama-3.3-70b-versatile",
     model_provider = "openai",
     base_url = "https://api.groq.com/openai/v1",
     api_key = qroq_api_key
)



# view definitions

def home():
    s.title("AI Enabled Resume Shortlisting Application for HR Teams")
    s.header("Welcome to Resume Management Application")
    s.markdown("Please select your prefered option from sidebar")


# Shortlist window
def shortlist_window():
    s.header("Welcome to resume shortlisting")

    HR_query = s.chat_input("HR Query: ")
    if HR_query:

        s.markdown(HR_query)

        # embed HR query
        query_embedding = embed_model.embed_query(HR_query)

        # similarity search
        # get top 4 results with similarity to given query_embedding
        results = collection.query( query_embeddings = [query_embedding], n_results = 3)


        # prompt for llm
        explanation_input = f"""
                You are an AI HR Assistant with 10+ years of recruitment experience.
                Your role is STRICTLY LIMITED to recruitment and resume shortlisting tasks.

                ========================
                IMPORTANT RULES (MUST FOLLOW)
                1. ONLY answer recruitment or HR-related queries.
                2. If the query is NOT related to: hiring, recruitment, resume shortlisting, candidate selection, skills, experience, job roles
                then DO NOT analyze resumes.
                3. DO NOT provide general knowledge answers.
                4. DO NOT add explanations, assumptions, or extra text.

                If the query is NOT a recruitment or HR-related question, respond with EXACTLY this sentence and NOTHING ELSE:
                "Please ask a recruitment or HR-like question."

                ========================
                VALID HR QUERY BEHAVIOR
                If the query IS a valid recruitment question:
                - You will receive the TOP 3 applicant resumes.
                - Analyze ONLY the provided resumes.
                - Select ONLY the top 1 or top 2 most suitable candidates.
                - Use ONLY the information present in the resumes.
                - Do NOT hallucinate or add missing details.

                ========================
                OUTPUT:
                If HR query is VALID give
                Selected Applicant(s) information including Name,Email, Mobile Number,Skills, Experience, Resume ID, Resume Path, Resume Metadata
                in structured format.

                Why Selected:
                -clear justification based ONLY on skills and experience.
                Why Not Selected:
                - reason for each non-selected applicant.

                ========================
                INPUT DATA
                HR Query:{HR_query}
                Top Applicant Resumes (JSON):{json.dumps(results)}

                """
        result = llm.invoke(explanation_input)
        explanation_output = result.content.strip()
        # s.subheader("Assistant")
        

        s.markdown("Results: ")
        s.write(explanation_output)
        # for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        #     s.markdown("Metadata:")
        #     s.markdown(meta)
        #     s.markdown("Document:")
        #     s.markdown(doc)




def load_pdf_resume(pdf_path, resume_id):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    resume_content = ""

    for page in docs:
        resume_content += page.page_content

    metadata = {
        "source": resume_id,
        "page_count": len(docs)
    }

    return resume_content, metadata


def manage_resumes_window():
    s.header("Welcome to Resume management portal")
    s.subheader("Select your prefered option....")

    s.subheader("## Upload new resumes ")
    # get resume file from user
    uploaded_resume = s.file_uploader("Upload resume file", type = ["pdf"], key = "upload_new_resume")

    if uploaded_resume:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_resume.getvalue())
            temp_file_path = tmp_file.name
            s.session_state.filepath = temp_file_path

        resume_id = Path(uploaded_resume.name).stem
        # s.write("ResumeID = ", resume_id)
        
        s.success("Resume uploaded successfully....")
    
        store_btn = s.button("Store embeddings to database", type= "primary")
        if store_btn:

            resume_text, resume_info = load_pdf_resume(s.session_state.filepath, resume_id)
            # s.success("File embedddings stored to database.")
            # s.write(resume_text)

            # create resume embeddings
            resume_embeddings = embed_model.embed_documents([resume_text])

            # add embeddings and other data (collection) to chromadb
            collection.add(
                ids = [resume_id], 
                embeddings = resume_embeddings, 
                metadatas = [resume_info], 
                documents = [resume_text]
            )
            s.success("File is stored with id: ")
            s.success(resume_id)


            # release file path
            if "upload_new_resume" in s.session_state:
                del s.session_state["upload_new_resume"]
            s.session_state.filepath = temp_file_path
            s.rerun()

        
    
    # List all resumes
    s.subheader("## View all resumes")

    # view_res_btn = s.button("View all resumes", type = "primary")
    # if view_res_btn:
    all_data = collection.get()["ids"]

    if not all_data:
        s.info("No resumes found.")
    else:
        for resume_id in all_data:
            col1, col2, col3 = s.columns([4, 2, 2])

            col1.markdown(f"**{resume_id}**")

            # update button
            if col2.button("Update", key = f"update_{resume_id}"):
                s.session_state.update_id = resume_id
                s.session_state.view = "update"
                s.rerun()

            if col3.button("Delete", key = f"delete_{resume_id}"):
                collection.delete(ids = [resume_id])
                s.toast(f"{resume_id} deleted successfully")
                s.rerun()



# Update resume window
def update_resume_window():

    s.subheader("Welcome to update resume window")

    view_btn = s.button("View all resume ids")
    if view_btn:
        all_ids = collection.get()["ids"]
        s.table(all_ids)
    
    if not s.session_state.update_id:
        update_res_id = s.text_input("Enter resume id to update resume")

        if update_res_id:
            all_resume_ids = collection.get()["ids"]
            if update_res_id not in all_resume_ids:
                s.error("Please enter valid resume id")
                return
            else:
                s.session_state.update_id = update_res_id
                s.rerun()
        return

    update_res_id =  s.session_state.update_id
    s.success(f"You are updating resume with id = {update_res_id}")

    s.markdown(f"Upload updated resume file with id {update_res_id}")
    uploaded_resume1 = s.file_uploader("Upload resume file", type = ["pdf"],key = "upload_updated_resume")

    if uploaded_resume1:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_resume1.getvalue())
            temp_file_path = tmp_file.name
            s.session_state.filepath = temp_file_path

        resume_id = update_res_id
        s.success("Resume uploaded successfully....")

        
        store_btn = s.button("Store updated resume embeddings to database", type= "primary")
        if store_btn:

            try:


                resume_text, resume_info = load_pdf_resume(s.session_state.filepath, resume_id)
                # s.success("File embedddings stored to database.")
                # s.write(resume_text)

                # create resume embeddings
                resume_embeddings = embed_model.embed_documents([resume_text])
            
           
            except Exception as e:
                s.error("Please connect to embedding model")
                s.stop()

            # delete old resume
            collection.delete(ids=[update_res_id])


            # add embeddings and other data (collection) to chromadb
            collection.add(
                ids = [resume_id], 
                embeddings = resume_embeddings, 
                metadatas = [resume_info], 
                documents = [resume_text]
             )


            s.success("File is stored with id: ")
            s.success(resume_id)

            if "upload_update_resume" in s.session_state:
                del s.session_state["upload_updated_resume"]
            
            s.session_state.update_id = None
            s.session_state.view = "manage"
            s.rerun()
            



# UI

with s.sidebar:
    home_btn = s.button("Home", type = "primary")
    if home_btn:
        s.session_state.view = "main"


    shortlist_btn = s.button("Shortlist resumes",type= "secondary")
    if shortlist_btn:
        s.session_state.view = "shortlist"
    
    mng_resumes_btn = s.button("Manage resumes", type = "primary")
    if mng_resumes_btn:
        s.session_state.view = "manage"

    update_resume_btn = s.button("Update resume",type= "secondary")
    if update_resume_btn:
        s.session_state.view = "update"

    

    


# managing session state

if s.session_state.view == "main":
    home()
if s.session_state.view == "shortlist":
    shortlist_window()
if s.session_state.view == "manage":
    manage_resumes_window()
if s.session_state.view == "update":
    update_resume_window()