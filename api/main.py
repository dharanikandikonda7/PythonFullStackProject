import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client

# Load Supabase credentials
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("❌ Missing Supabase credentials in .env file")

sb = create_client(url, key)

# FastAPI setup
app = FastAPI(title="Flashcard Q&A API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Flashcard Manager
# -----------------------------
class FlashcardManager:
    def __init__(self):
        self.table = sb.table("flashcards")

    def get_all(self):
        result = self.table.select("*").execute()
        return result.data or []

    def add(self, question, answer, source="manual"):
        result = self.table.insert({
            "question": question,
            "answer": answer,
            "source": source
        }).execute()
        return result.data

# -----------------------------
# Progress Manager
# -----------------------------
class ProgressManager:
    def __init__(self):
        self.table = sb.table("progress")

    def record_result(self, flashcard_id, is_correct: bool):
        result = self.table.insert({
            "flashcard_id": flashcard_id,
            "is_correct": is_correct
        }).execute()
        return result.data

    def get_all(self):
        result = self.table.select("*").execute()
        return result.data or []

# -----------------------------
# PDF Upload Manager
# -----------------------------
class PDFManager:
    def __init__(self):
        self.table = sb.table("uploaded_pdfs")

    def record_upload(self, file_name, user_id=None):
        result = self.table.insert({
            "file_name": file_name,
            "user_id": user_id
        }).execute()
        return result.data

# Managers
flashcard_manager = FlashcardManager()
progress_manager = ProgressManager()
pdf_manager = PDFManager()

# -----------------------------
# API Endpoints
# -----------------------------
@app.get("/")
def root():
    return {"message": "✅ Flashcard API is running"}

@app.get("/flashcards")
def get_flashcards():
    data = flashcard_manager.get_all()
    if not data:
        raise HTTPException(status_code=404, detail="No flashcards found")
    return data

@app.post("/flashcards/add")
def add_flashcard(question: str, answer: str):
    result = flashcard_manager.add(question, answer)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to add flashcard")
    return {"message": "✅ Flashcard added successfully!"}

@app.post("/progress")
def save_progress(flashcard_id: int, is_correct: bool):
    result = progress_manager.record_result(flashcard_id, is_correct)
    return {"message": "Progress saved", "data": result}

@app.get("/progress")
def get_progress():
    return progress_manager.get_all()
