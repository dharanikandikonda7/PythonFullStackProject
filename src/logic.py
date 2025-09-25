# src/logic.py

'''
# ---------CREATE-----------
def add_task(self, name, duration_days):
    """
    Add a new membership_plan to the database.
    Return the success message if task is added.
    """
    if not name or not duration_days:
        return {"Success": False, "message": "Name & Duration are required"}

    # Call DB method to insert task
    result = self.db.create_plan(name, duration_days)

    if result.get("Success"):
        return {"Success": True, "message": "Plan added successfully"}
    else:
        return {"Success": False, "message": f"Error: {result.get('error')}"}
'''

# src/logic.py
from src.db import DatabaseManager

# ---------------- FLASHCARDS ----------------
class FlashcardManager:
    """ Handles flashcard operations: add, fetch all, fetch by ID, delete. """
    def __init__(self):
        self.db = DatabaseManager()

    def add_flashcard(self, question: str, answer: str, source: str = "manual"):
        """Add a new flashcard."""
        if not question or not answer:
            return {"Success": False, "message": "Question & Answer are required"}
        result = self.db.add_flashcard(question, answer, source)
        if result:
            return {"Success": True, "message": "Flashcard added successfully"}
        return {"Success": False, "message": "Failed to add flashcard"}

    def get_flashcards(self):
        """Fetch all flashcards."""
        result = self.db.get_flashcards()
        if result:
            return {"Success": True, "data": result}
        return {"Success": False, "message": "No flashcards found"}

    def get_flashcard_by_id(self, card_id: int):
        """Fetch flashcard by ID."""
        result = self.db.get_flashcard_by_id(card_id)
        if result:
            return {"Success": True, "data": result[0]}  # return single item
        return {"Success": False, "message": "Flashcard not found"}

    def delete_flashcard(self, card_id: int):
        """Delete flashcard by ID."""
        result = self.db.delete_flashcard(card_id)
        if result:
            return {"Success": True, "message": "Flashcard deleted successfully"}
        return {"Success": False, "message": "Failed to delete flashcard"}

# ---------------- PROGRESS ----------------
class ProgressManager:
    """ Handles quiz progress operations: record progress, get all attempts, get wrong attempts. """
    def __init__(self):
        self.db = DatabaseManager()

    def add_progress(self, flashcard_id: int, is_correct: bool):
        """Record a quiz attempt for a flashcard."""
        if flashcard_id is None:
            return {"Success": False, "message": "Flashcard ID is required"}
        result = self.db.record_progress(flashcard_id, is_correct)
        if result:
            return {"Success": True, "message": "Progress recorded successfully"}
        return {"Success": False, "message": "Failed to record progress"}

    def get_all_progress(self):
        """Fetch all progress entries."""
        result = self.db.get_progress()
        if result:
            return {"Success": True, "data": result}
        return {"Success": False, "message": "No progress found"}

    def get_wrong_flashcard_ids(self):
        """Fetch IDs of flashcards answered incorrectly at least once."""
        result = self.db.get_wrong_attempts()
        if result:
            return {"Success": True, "data": result}
        return {"Success": False, "message": "No wrong flashcards found"}

# ---------------- UPLOADED PDFS ----------------
class PDFManager:
    """ Handles uploaded PDF metadata operations: add PDF, fetch all, delete PDF. """
    def __init__(self):
        self.db = DatabaseManager()

    def add_uploaded_pdf(self, file_name: str, user_id: int = None):
        """Store metadata of uploaded PDF."""
        if not file_name:
            return {"Success": False, "message": "File name is required"}
        result = self.db.add_uploaded_pdf(file_name, user_id)
        if result:
            return {"Success": True, "message": "PDF metadata stored successfully"}
        return {"Success": False, "message": "Failed to store PDF metadata"}

    def get_uploaded_pdfs(self):
        """Fetch all uploaded PDFs metadata."""
        result = self.db.get_uploaded_pdfs()
        if result:
            return {"Success": True, "data": result}
        return {"Success": False, "message": "No uploaded PDFs found"}

    def delete_uploaded_pdf(self, pdf_id: int):
        """Delete uploaded PDF metadata by ID."""
        result = self.db.delete_uploaded_pdf(pdf_id)
        if result:
            return {"Success": True, "message": "Uploaded PDF deleted successfully"}
        return {"Success": False, "message": "Failed to delete PDF metadata"}
