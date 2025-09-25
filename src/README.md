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
git clone <repository-url>

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

The app will open inyour browser at `http://localhost:8501`

## FastAPI Backend

cd api
python main.py

The app will be available at `http://localhost:8501`

### How to use

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
        make sure you've

## Future Enhancements
 
 Ideas for extending the Flashcard Quiz App:
**Multi-User Support**: Enable login/signup so multiple users can manage their own flashcards and progress.

**Flashcard Categories / Topics**: Organize flashcards by subjects (e.g., Math, History) and allow category-based quizzes.

**Analytics Dashboard**: Show charts for quizzes taken, correct vs incorrect answers, and performance trends over time.

**Spaced Repetition**: Use algorithms to repeat difficult flashcards more frequently for better retention.

**Enhanced PDF Processing**: Automatically generate Q&A from PDFs, highlight key terms, and create multiple-choice questions.

**Mobile-Friendly Interface**: Optimize layout for phones and tablets for on-the-go studying.

**Export / Import Flashcards**: Allow saving and loading flashcards via CSV or JSON files.

**Gamification**: Add badges, streaks, or rewards to motivate regular practice.



## Support

If you encounter any issues or have questions:
dharanikandikonda7@gmail.com








