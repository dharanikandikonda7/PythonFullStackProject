import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb = create_client(url, key)


class FlashcardManager:
    def __init__(self):
        self.table = sb.table("flashcards")

    def add_flashcard(self, question, answer):
        result = self.table.insert({"question": question, "answer": answer}).execute()
        return result.data

    def get_flashcards(self):
        result = self.table.select("*").execute()
        return result.data

    def get_flashcard(self, flashcard_id: int):
        result = self.table.select("*").eq("id", flashcard_id).execute()
        return result.data[0] if result.data else {"error": "Not found"}

    def delete_flashcard(self, flashcard_id: int):
        result = self.table.delete().eq("id", flashcard_id).execute()
        return {"message": "Deleted"} if result.data else {"error": "Not found"}


class ProgressManager:
    def __init__(self):
        self.table = sb.table("progress")

    def mark_correct(self, flashcard_id: int):
        sb.table("progress").update({"correct": sb.func.coalesce("correct", 0) + 1}).eq("flashcard_id", flashcard_id).execute()
        return {"message": "Marked correct"}

    def mark_wrong(self, flashcard_id: int):
        sb.table("progress").update({"wrong": sb.func.coalesce("wrong", 0) + 1}).eq("flashcard_id", flashcard_id).execute()
        return {"message": "Marked wrong"}

    def get_progress(self, flashcard_id: int):
        result = self.table.select("*").eq("flashcard_id", flashcard_id).execute()
        return result.data[0] if result.data else {"error": "No progress found"}


class PDFManager:
    def export_flashcards(self, flashcards, filename="flashcards.pdf"):
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        y = height - 50

        for card in flashcards:
            c.drawString(50, y, f"Q: {card['question']}")
            y -= 20
            c.drawString(50, y, f"A: {card['answer']}")
            y -= 40
            if y < 100:
                c.showPage()
                y = height - 50

        c.save()
        return {"message": f"Exported to {filename}"}
