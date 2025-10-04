import streamlit as st
import requests
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="Flashcard Q&A", page_icon="🧠")

# Initialize Session
if "flashcards" not in st.session_state:
    try:
        res = requests.get(f"{API_URL}/flashcards")
        if res.status_code == 200:
            st.session_state.flashcards = res.json()
        else:
            st.session_state.flashcards = []
    except Exception as e:
        st.error("⚠️ Backend not reachable. Start FastAPI server first.")
        st.stop()

if "index" not in st.session_state:
    st.session_state.index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = 0

# Sidebar Menu
st.sidebar.title("📚 Flashcard App")
menu = st.sidebar.radio("Navigate", ["Quiz", "Add Flashcard", "Progress"])

# QUIZ
if menu == "Quiz":
    st.title("📝 Flashcard Q&A")
    if not st.session_state.flashcards:
        st.warning("⚠️ No flashcards available. Please add some from the sidebar.")
    else:
        cards = st.session_state.flashcards
        card = cards[st.session_state.index]
        st.subheader(f"Question {st.session_state.index+1}/{len(cards)}")
        st.write(card["question"])

        ans = st.text_input("Your Answer:", key=f"answer_{st.session_state.index}")
        col1, col2 = st.columns(2)

        if col1.button("Submit"):
            st.session_state.answered += 1
            correct = ans.strip().lower() == card["answer"].strip().lower()
            if correct:
                st.session_state.score += 1
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Wrong! Correct Answer: {card['answer']}")
            requests.post(f"{API_URL}/progress", params={"flashcard_id": card["id"], "is_correct": correct})

        if col2.button("Next"):
            st.session_state.index = (st.session_state.index + 1) % len(cards)
            st.rerun()

# ADD FLASHCARD
elif menu == "Add Flashcard":
    st.title("➕ Add Flashcard")
    q = st.text_input("Question")
    a = st.text_input("Answer")
    if st.button("Add"):
        if q and a:
            res = requests.post(f"{API_URL}/flashcards/add", params={"question": q, "answer": a})
            if res.status_code == 200:
                st.success("✅ Flashcard added successfully!")
                st.session_state.flashcards = requests.get(f"{API_URL}/flashcards").json()
            else:
                st.error("⚠️ Failed to add flashcard.")
        else:
            st.warning("⚠️ Enter both question and answer.")

# PROGRESS
elif menu == "Progress":
    st.title("📊 Your Progress")

    if st.session_state.answered > 0:
        correct = st.session_state.score
        incorrect = st.session_state.answered - correct
        accuracy = (correct / st.session_state.answered) * 100

        st.write(f"✅ Correct: {correct}")
        st.write(f"❌ Incorrect: {incorrect}")
        st.write(f"📈 Accuracy: {accuracy:.2f}%")

        # Pie Chart for performance visualization
        labels = ["Correct", "Incorrect"]
        values = [correct, incorrect]
        colors = ["#4CAF50", "#F44336"]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
        ax.axis("equal")  # Equal aspect ratio ensures the pie is circular
        st.pyplot(fig)
    else:
        st.info("⚠️ No quiz attempts yet.")