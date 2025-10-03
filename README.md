# 📚 Flashcard Quiz App with PDF Upload

## Project Description

Flashcard Quiz App is a full-stack web application built with **Python (Streamlit)** and **Supabase**.  
It helps users study efficiently by creating and reviewing flashcards. Users can **manually add flashcards** or **upload PDFs** to extract content and generate flashcards automatically.  
  

## Project Features

### Core Features
- **Add Flashcards Manually:** Create custom Q&A pairs.  
- **Upload PDFs:** Extract text and optionally generate flashcards automatically.  
- **Quiz Mode:** Randomized questions with immediate feedback.  
- **Review Mode:** Retry flashcards answered incorrectly.  
- **Persistent Data Storage:** All flashcards and progress stored in Supabase.  

## Project structure
FLASHCARDQ&A/
|
|---src/           # Core application logic
|   |---logic.py   # Business logic and task
operations
|   |---db.py      # DataBase operations
|  
|---api/          # Backend API
|   |---main.py   # FastAPI endpoints
|
|---frontend/     # Frontend application
|   |---app.py    # Streamlit web interface
|
|---requirements.txt  # Install python dependencies
|
|---README.md     # Project Documentation
|
|---.env          # Python Variables (supabase)




## Quick Start

### Prerequisites

- Python 3.8 or higher
- A Supabase Acoount
- Git (Push/Pull/Clone)

### 1. Clone or Download the Project
# Option 1: Clone with Git
git clone https://github.com/dharanikandikonda7/PythonFullStackProject

# Option 2: Download and extract the ZIP file

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Set Up Supabase Database

1.Create a Supabase Project:

2. create the Tasks Table:

- Go to the SQL Editor in your Supabase dashboard
- Run this SQL Command:

``` sql

-- Table for flashcards
CREATE TABLE flashcards (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    source TEXT DEFAULT 'manual',  -- 'manual' or 'pdf'
    created_at TIMESTAMP DEFAULT NOW()
);

-- Progress
CREATE TABLE progress (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    flashcard_id BIGINT REFERENCES flashcards(id) ON DELETE CASCADE,
    is_correct BOOLEAN NOT NULL,
    attempted_at TIMESTAMP DEFAULT NOW()
);

-- Upload PDFs
CREATE TABLE uploaded_pdfs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    file_name TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT NOW(),
    user_id BIGINT NULL  -- Optional, for multi-user support
);

```

3. **Get Your Credintials:**

### 4. configure Environment Variables

1. create a `.env` file in the project root

2. Add Your Supabase credentials to `.env`:
SUPABASE_URL=YOUR_PROJECT_URL_HERE
SUPABASE_KEY=YOUR_ANON_KEY_HERE

### 5. Run the Application

## Streamlit Fronted
streamlit run frontend/app.py

The app will open inyour browser at `http://localhost:8000`

## FastAPI Backend

cd api
python main.py

The app will be available at `http://localhost:8000`

### How to use

Add flashcards manually or upload PDFs

Start a quiz session to practice questions

Submit your answers and get instant feedback

Track your progress with performance graphs

## Techical Details

### Techologies Used

  **Frontend**: Streamlit (Python-based interactive web interface)

  **Backend**: Python (handles quiz logic, PDF processing, and communication with Supabase)

  **Database**: Supabase (PostgreSQL) – stores flashcards, quiz progress, and optional PDF metadata

  **Programming Language**: Python

### Key Components

1. **`src/db.py`**:Database operations Handles all CRUD operations with Supabase

2. **`src/logic.py`**: Business logic Task validation and Processing

3. **`api/main.py`**: Backend API. Contains FastAPI endpoints to interact with the frontend and database.

4. **`frontend/app.py`**: Frontend application. Streamlit interface for users to interact with the Flashcard Q&A system.

5. **`requirements.txt`**: Python dependencies. Lists all required packages for the project.

6. **`.env`**: Environment variables. Stores sensitive configuration like Supabase keys and API credentials.

7. **`README.md`**: Project documentation. Contains overview, setup instructions, and usage details.


## Troubleshooting

## Common Issues

1. **"Module not found" errors**  
    make sure you've installed all Python dependencies and that Python can find your packages.  
    - Install deps:  
      ```bash
      pip install -r requirements.txt
      ```
    - Ensure your package folders are importable (either add `__init__.py` files or run with the project root on `PYTHONPATH`). Examples:
      - Add `__init__.py` (empty) to `api/` and `src/`.
      - Or set `PYTHONPATH` (mac / linux):
        ```bash
        export PYTHONPATH=$(pwd)
        uvicorn api.main:app --reload --port 8000
        ```
        (PowerShell)
        ```powershell
        $env:PYTHONPATH = (Get-Location).Path
        uvicorn api.main:app --reload --port 8000
        ```
    - If you use relative imports, run uvicorn with module form from project root:
      ```bash
      uvicorn api.main:app --reload --port 8000
      ```

2. **Supabase connection errors / invalid credentials**  
    make sure you've added correct Supabase variables to `.env` and loaded them.  
    - `.env` should include:
      ```env
      SUPABASE_URL=https://your-project.supabase.co
      SUPABASE_KEY=your_anon_or_service_key
      ```
    - Verify the values are not expired/rotated and that your network allows outbound HTTPS to Supabase.

3. **"Could not find table 'public.xxx' / SQL errors**  
    make sure you've created the required tables in Supabase (run the SQL in the README).  
    - Double-check table names and schema (usually `public`).  
    - Run the SQL in Supabase → SQL Editor and confirm tables exist.

4. **Streamlit: `File does not exist: app.py`**  
    make sure you run Streamlit from the folder containing `app.py`, or provide full path:  
    ```bash
    # if app.py is inside frontend/
    streamlit run frontend/app.py
    ```
    run `dir` (Windows) or `ls` (mac/linux) to confirm file location.

5. **Uvicorn import / relative import errors**  
    common cause: running from wrong directory or missing `__init__.py`.  
    - Use absolute imports (`from src.logic import ...`) and run from project root.  
    - Or run with `python -m uvicorn api.main:app --reload` to ensure package imports resolve.

6. **Port already in use**  
    change port or kill existing process. Example (Windows):
    ```powershell
    netstat -ano | findstr 8000
    taskkill /PID <pid> /F
    ```
    or start uvicorn on a different port:
    ```bash
    uvicorn api.main:app --reload --port 8001
    ```

7. **CORS errors when frontend calls backend**  
    ensure your FastAPI has CORS configured (allow origins for Streamlit). Example in `api/main.py`:
    ```python
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8501","http://127.0.0.1:8501"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    ```

8. **PDF upload / PyPDF2 extraction errors**  
    - Verify the uploaded file is a valid PDF and saved successfully before processing.  
    - For large PDFs, processing may take time—check server logs and increase timeouts if needed.  
    - Confirm `PyPDF2` version in `requirements.txt` and that it is installed.

9. **OneDrive / Windows file-lock & permission issues**  
    if your project is inside OneDrive, files may be locked or synced. Try moving the project to a non-OneDrive folder (e.g., `C:\projects\FlashCardQ&A`) and re-run.

10. **API returns unexpected JSON / frontend errors when parsing**  
    - Inspect API response with `print(resp.status_code, resp.text)` in the frontend or use Postman/curl to check exact shape.  
    - Make sure frontend `requests` code expects the same structure your backend returns (e.g., `{"Success": True, "data": [...]}` vs `[...]`).

---

## Quick Debug Steps (summary)
- Activate virtual env: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (mac/linux)  
- Install deps: `pip install -r requirements.txt`  
- Confirm `.env` values and restart server(s).  
- Start backend from project root: `uvicorn api.main:app --reload --port 8000`  
- Start frontend with correct path: `streamlit run frontend/app.py`  
- If something fails, copy & paste the *full traceback* into the issue — that makes fixing much faster.

---

## Future Enhancements

- **Multi-User Support (Auth & Profiles)**  
  Add sign-up / sign-in (JWT or Supabase Auth) so each user has a personal set of flashcards and progress.

- **Flashcard Categories / Topics**  
  Add a `topic` column and UI filters so users can choose a subject-specific quiz.

- **Spaced Repetition Scheduler**  
  Implement an SRS algorithm (e.g., SM-2) to surface cards at optimal intervals for retention.

- **Analytics Dashboard**  
  Track per-user metrics: daily accuracy, average response time, most-missed cards; show charts and trends.

- **Enhanced PDF Processing**  
  Improve Q&A generation using NLP (OpenAI or local ML models): extract key sentences, generate Q/A, and optional multiple-choice.

- **Import / Export (CSV / JSON)**  
  Allow users to import large decks or export their decks and progress for backup or sharing.

- **Mobile-Friendly UI**  
  Improve responsive layout and test on mobile browsers (or create a PWA).

- **Gamification**  
  Badges, streaks, leaderboards, and small rewards to motivate daily practice.

- **Offline Mode / Local Cache**  
  Keep a lightweight local cache of flashcards so users can practice without a network connection, syncing when back online.

- **Role-based Admin Panel**  
  Admin UI to moderate uploaded PDFs, review auto-generated flashcards and manage content quality.

---

## Support

If you encounter any issues or have questions:
dharanikandikonda7@gmail.com








