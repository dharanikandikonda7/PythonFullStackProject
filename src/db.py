# src/db.py
import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Create client that interacts with Supabase
supabase = create_client(url, key)


class DatabaseManager:
    # ----------------
    # Flashcard operations
    # ----------------
    def add_flashcard(self, question: str, answer: str, source: str = "manual"):
        """Insert a new flashcard."""
        response = supabase.table("flashcards").insert({
            "question": question,
            "answer": answer,
            "source": source
        }).execute()
        return response.data

    def get_flashcards(self):
        """Fetch all flashcards."""
        response = supabase.table("flashcards").select("*").order("created_at").execute()
        return response.data

    def get_flashcard_by_id(self, card_id: int):
        """Fetch a single flashcard by ID."""
        response = supabase.table("flashcards").select("*").eq("id", card_id).execute()
        return response.data

    def delete_flashcard(self, card_id: int):
        """Delete a flashcard by ID."""
        response = supabase.table("flashcards").delete().eq("id", card_id).execute()
        return response.data

    # ---------------
    # Progress operations
    # ---------------
    def record_progress(self, flashcard_id: int, is_correct: bool):
        """Record quiz progress for a flashcard."""
        response = supabase.table("progress").insert({
            "flashcard_id": flashcard_id,  # fixed typo here
            "is_correct": is_correct
        }).execute()
        return response.data

    def get_progress(self):
        """Fetch all progress entries ordered by attempt time desc."""
        response = supabase.table("progress").select("*").order("attempted_at", desc=True).execute()
        return response.data

    def get_wrong_attempts(self):
        """Fetch flashcard IDs answered incorrectly at least once."""
        response = supabase.table("progress").select("flashcard_id").eq("is_correct", False).execute()
        # Extract unique flashcard IDs
        ids = list({rec["flashcard_id"] for rec in response.data})
        return ids

    # --------------
    # Uploaded PDFs operations
    # --------------
    def add_uploaded_pdf(self, file_name: str, user_id: int = None):
        """Insert metadata of uploaded PDF."""
        response = supabase.table("uploaded_pdfs").insert({
            "file_name": file_name,
            "user_id": user_id
        }).execute()
        return response.data

    def get_uploaded_pdfs(self):
        """Fetch all uploaded PDFs metadata ordered by uploaded_at desc."""
        response = supabase.table("uploaded_pdfs").select("*").order("uploaded_at", desc=True).execute()
        return response.data

    def delete_uploaded_pdf(self, pdf_id: int):
        """Delete uploaded PDF metadata by ID."""
        response = supabase.table("uploaded_pdfs").delete().eq("id", pdf_id).execute()
        return response.data
