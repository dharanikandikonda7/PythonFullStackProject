#db_manager.py
import os
from supabase import create_client
from dotenv import load_dotenv

# loading environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# create client that interacts with the supabase
supabase= create_client(url,key)

#create Task
'''def create_task(title,descriptikon,duedate,ptiority=):
    return supabse.table("tasks").insert({
        "title":title,
        "description":descipyion,
        .
        .
        .
        "completed":False
    }).execute
#Get All Tasks
def get_add_flashcards():
    return supabase.table("flashcards").select(*).order("").execute
    ()

#Update task status
def Update_flashcards():
    return supabase.table("flashcards").Update({"completed":completed}).eq("id",task_id).execute()

#Delete flashcard
def delete_flashcard(task_id):
    return supabase.table("flashcards").delete().eq("id",task_id).execute()
'''

# ---------------- 
# flashcard table operations
# ----------------

# Create flashcard
def add_flashcard(question: str, answer: str, source: str = "manual"):
    """Insert a new flashcard."""
    response = supabase.table("flashcards").insert({
        "question": question,
        "answer": answer,
        "source": source
    }).execute()
    return response.data

# Get flashcard
def get_flashcards():
    """Fetch all flashcards."""
    response = supabase.table("flashcards").select("*").order("created_at").execute()
    return response.data

# Get flashcard by id
def get_flashcard_by_id(card_id: int):
    """Fetch a single flashcard by ID."""
    response = supabase.table("flashcards").select("*").eq("id", card_id).execute()
    return response.data

# Delete flashcard
def delete_flashcard(card_id: int):
    """Delete a flashcard by ID."""
    response = supabase.table("flashcards").delete().eq("id", card_id).execute()
    return response.data


#---------------
#progress table operations
#---------------
'''CREATE TABLE progress (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    flashcard_id BIGINT REFERENCES flashcards(id) ON DELETE CASCADE,
    is_correct BOOLEAN NOT NULL,
    attempted_at TIMESTAMP DEFAULT NOW()
);'''

def record_progress(flashcard_id,is_correct):
    """Record quiz progress for a flashcard."""
    return supabase.table("progress").insert({
        "flascard_id":flashcard_id,
        "is_correct":is_correct
    }).execute

def get_progress():
    response = supabase.table("progress").select("*").order("attempted_at",desc=True).execute()
    return response.data

def get_wrong_attempts():
    #Fetch flashcards answered incorrectly (for review mode).
    response=supabase.table("progress").select("flashcard_id").eq("is_correct",False).execute()
    return [rec["flashcard_id"] for rec in response.data]

#------------
#uploaded_pdfs table operations
#------------
'''CREATE TABLE uploaded_pdfs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    file_name TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT NOW(),
    user_id BIGINT NULL  -- Optional, for multi-user support
);'''

def add_uploaded_pdf(file_name,user_id):
    #Insert metadata of uploaded PDF.
    response=supabase.table("uploaded_pdfs").insert({
        "file_name":file_name,
        "user_id":user_id
    }).execute()
    return response.data

def get_uploaded_pdfs():
    #Fetch all uploaded PDFs metadata.
    response=supabase.table("unploaded_pdfs").select("*").order("uploaded_at",desc=True).execute()
    return response.data

def delete_uploaded_pdf(pdf_id):
    #uploaded_pdfs table operations
    rsponse=supabase.table("uploaded_pdfs").delete().eq("id",pdf_id).execute()
    return response.data

