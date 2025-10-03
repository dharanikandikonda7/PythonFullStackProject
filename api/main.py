from fastapi import FastAPI
from src.logic import FlashcardManager, ProgressManager, PDFManager

app = FastAPI()
flashcard_manager = FlashcardManager()
progress_manager = ProgressManager()
pdf_manager = PDFManager()

@app.get("/")
def home():
    return {"message": "Flashcard API running with Supabase"}

@app.post("/flashcards/")
def add_flashcard(question: str, answer: str):
    return flashcard_manager.add_flashcard(question, answer)

@app.get("/flashcards/")
def list_flashcards():
    return flashcard_manager.get_flashcards()

@app.get("/flashcards/{flashcard_id}")
def get_flashcard(flashcard_id: int):
    return flashcard_manager.get_flashcard(flashcard_id)

@app.delete("/flashcards/{flashcard_id}")
def delete_flashcard(flashcard_id: int):
    return flashcard_manager.delete_flashcard(flashcard_id)

@app.post("/progress/{flashcard_id}/correct")
def mark_correct(flashcard_id: int):
    return progress_manager.mark_correct(flashcard_id)

@app.post("/progress/{flashcard_id}/wrong")
def mark_wrong(flashcard_id: int):
    return progress_manager.mark_wrong(flashcard_id)

@app.get("/progress/{flashcard_id}")
def get_progress(flashcard_id: int):
    return progress_manager.get_progress(flashcard_id)

@app.get("/export/pdf")
def export_pdf():
    flashcards = flashcard_manager.get_flashcards()
    return pdf_manager.export_flashcards(flashcards)
