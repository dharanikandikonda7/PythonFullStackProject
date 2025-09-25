# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sys
import os

# Import your business logic classes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.logic import FlashcardManager, ProgressManager, PDFManager

# -------------------- App Setup ------------------------------
app = FastAPI(title="Flash Card Quiz API", version="1.0")

# Allow frontend (Streamlit/React) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate managers
flashcard_manager = FlashcardManager()
progress_manager = ProgressManager()
pdf_manager = PDFManager()

# ------ Data Models -------

# Flashcards
class FlashcardCreate(BaseModel):
    question: str
    answer: str
    source: Optional[str] = "manual"

# Progress
class ProgressCreate(BaseModel):
    flashcard_id: int
    is_correct: bool

# Uploaded PDFs
class UploadedPDFCreate(BaseModel):
    file_name: str
    user_id: Optional[int] = None

# -------------------- API Endpoints -------------------------

# --- Home ---
@app.get("/")
def home():
    """Check if the API is running."""
    return {"message": "Flashcard Quiz API is running"}

# --- Flashcards ---
@app.get("/flashcards")
def get_flashcards():
    result = flashcard_manager.get_flashcards()
    if result.get("Success"):
        return result
    raise HTTPException(status_code=404, detail=result.get("message"))

@app.get("/flashcards/{flashcard_id}")
def get_flashcard(flashcard_id: int):
    result = flashcard_manager.get_flashcard_by_id(flashcard_id)
    if result.get("Success"):
        return result
    raise HTTPException(status_code=404, detail=result.get("message"))

@app.post("/flashcards")
def create_flashcard(flashcard: FlashcardCreate):
    result = flashcard_manager.add_flashcard(flashcard.question, flashcard.answer, flashcard.source)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.delete("/flashcards/{flashcard_id}")
def delete_flashcard(flashcard_id: int):
    result = flashcard_manager.delete_flashcard(flashcard_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

# --- Progress ---
@app.post("/progress")
def add_progress(progress: ProgressCreate):
    """Record a quiz attempt for a flashcard."""
    result = progress_manager.add_progress(progress.flashcard_id, progress.is_correct)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.get("/progress")
def get_all_progress():
    """Fetch all progress entries."""
    result = progress_manager.get_all_progress()
    if result.get("Success"):
        return result
    raise HTTPException(status_code=404, detail=result.get("message"))

@app.get("/progress/wrong-flashcards")
def get_wrong_flashcards():
    """Fetch flashcard IDs answered incorrectly at least once."""
    result = progress_manager.get_wrong_flashcard_ids()
    if result.get("Success"):
        return result
    raise HTTPException(status_code=404, detail=result.get("message"))

# --- Uploaded PDFs ---
@app.post("/pdfs")
def add_uploaded_pdf(pdf: UploadedPDFCreate):
    """Store metadata of uploaded PDF."""
    result = pdf_manager.add_uploaded_pdf(pdf.file_name, pdf.user_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.get("/pdfs")
def get_uploaded_pdfs():
    """Fetch all uploaded PDFs metadata."""
    result = pdf_manager.get_uploaded_pdfs()
    if result.get("Success"):
        return result
    raise HTTPException(status_code=404, detail=result.get("message"))

@app.delete("/pdfs/{pdf_id}")
def delete_uploaded_pdf(pdf_id: int):
    """Delete uploaded PDF metadata by ID."""
    result = pdf_manager.delete_uploaded_pdf(pdf_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

# ----- Run -----
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
