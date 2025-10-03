# src/db.py
import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # For Q&A generation

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class DatabaseManager:
    # ---------------- Flashcard operations ----------------
    def add_flashcard(self, question: str, answer: str, topic: str = None, source: str = "manual"):
        """Insert a new flashcard."""
        data = {
            "question": question,
            "answer": answer,
            "topic": topic,
            "source": source
        }
        response = supabase.table("flashcards").insert(data).execute()
        return response.data

    def get_flashcards(self, topic: str = None):
        """Fetch all flashcards, optionally filtered by topic."""
        query = supabase.table("flashcards").select("*").order("created_at")
        if topic:
            query = query.eq("topic", topic)
        response = query.execute()
        return response.data

    def get_flashcard_by_id(self, card_id: int):
        response = supabase.table("flashcards").select("*").eq("id", card_id).execute()
        return response.data

    def delete_flashcard(self, card_id: int):
        response = supabase.table("flashcards").delete().eq("id", card_id).execute()
        return response.data

    # ---------------- Progress operations ----------------
    def record_progress(self, flashcard_id: int, is_correct: bool):
        response = supabase.table("progress").insert({
            "flashcard_id": flashcard_id,
            "is_correct": is_correct
        }).execute()
        return response.data

    def get_progress(self):
        response = supabase.table("progress").select("*").order("attempted_at", desc=True).execute()
        return response.data

    def get_wrong_attempts(self):
        response = supabase.table("progress").select("flashcard_id").eq("is_correct", False).execute()
        ids = list({rec["flashcard_id"] for rec in response.data})
        return ids

    # ---------------- Uploaded PDFs ----------------
    def add_uploaded_pdf(self, file_name: str, user_id: int = None):
        response = supabase.table("uploaded_pdfs").insert({
            "file_name": file_name,
            "user_id": user_id
        }).execute()
        return response.data

    def get_uploaded_pdfs(self):
        response = supabase.table("uploaded_pdfs").select("*").order("uploaded_at", desc=True).execute()
        return response.data

    def delete_uploaded_pdf(self, pdf_id: int):
        response = supabase.table("uploaded_pdfs").delete().eq("id", pdf_id).execute()
        return response.data
