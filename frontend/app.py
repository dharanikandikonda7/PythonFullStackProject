import streamlit as st
import requests
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"

# --------------------------
# Initialize Session State
# --------------------------
if "flashcards" not in st.session_state:
    try:
        resp = requests.get(f"{API_URL}/flashcards")
        st.session_state.flashcards = resp.json() if resp.status_code == 200 else []
    except:
        st.session_state.flashcards = []

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "show_result" not in st.session_state:
    st.session_state.show_result = False

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = 0


# --------------------------
# Sidebar Navigation
# --------------------------
st.sidebar.title("📚 Flashcard App")
menu = st.sidebar.radio("Navigate", ["Quiz", "Add Flashcard", "Progress"])

# --------------------------
# QUIZ MODE
# --------------------------
# --------------------------
# QUIZ MODE
# --------------------------
if menu == "Quiz":
    st.title("📝 Flashcard Q&A")

    if st.session_state.flashcards:
        idx = st.session_state.current_index

        # ✅ make sure index wraps around correctly
        if idx >= len(st.session_state.flashcards):
            st.success("🎉 Quiz Completed!")
            st.write(f"Your Score: {st.session_state.score}/{st.session_state.answered}")

            if st.button("🔄 Restart Quiz"):
                st.session_state.current_index = 0
                st.session_state.score = 0
                st.session_state.answered = 0
                st.session_state.show_result = False
                st.rerun()

        else:
            # ✅ always get the latest flashcard by index
            flashcard = st.session_state.flashcards[idx]
            question = flashcard["question"]
            answer = flashcard["answer"]

            st.subheader(f"Question {idx+1}/{len(st.session_state.flashcards)}")
            st.write(question)

            # ✅ force input to refresh each question by key
            user_answer = st.text_input(
                "Your Answer:", 
                key=f"answer_input_q{idx}"
            )

            col1, col2 = st.columns(2)

            if col1.button("Submit", key=f"submit_{idx}"):
                st.session_state.show_result = True
                st.session_state.answered += 1
                st.session_state.last_correct = (user_answer.strip().lower() == answer.strip().lower())
                if st.session_state.last_correct:
                    st.session_state.score += 1

            if col2.button("Next", key=f"next_{idx}"):
                st.session_state.current_index += 1
                st.session_state.show_result = False
                st.rerun()

            # ✅ show result feedback after submit
            if st.session_state.show_result:
                if st.session_state.last_correct:
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Wrong! Correct Answer: {answer}")

    else:
        st.warning("⚠️ No flashcards available. Please add some.")


# --------------------------
# ADD FLASHCARD
# --------------------------
elif menu == "Add Flashcard":
    st.title("➕ Add Flashcard")

    with st.form("add_flashcard_form"):
        question = st.text_input("Enter Question")
        answer = st.text_input("Enter Answer")
        submitted = st.form_submit_button("Add")

        if submitted:
            if question.strip() and answer.strip():
                resp = requests.post(f"{API_URL}/flashcards/add", params={"question": question, "answer": answer})
                if resp.status_code == 200:
                    st.success("✅ Flashcard added successfully!")
                    # Refresh flashcards
                    st.session_state.flashcards = requests.get(f"{API_URL}/flashcards").json()
                else:
                    st.error(f"⚠️ Failed to add flashcard: {resp.text}")
            else:
                st.error("⚠️ Both fields are required!")


# --------------------------
# PROGRESS
# --------------------------
elif menu == "Progress":
    st.title("📊 Your Progress")

    if st.session_state.answered > 0:
        accuracy = (st.session_state.score / st.session_state.answered) * 100
        st.write(f"✅ Correct: {st.session_state.score}")
        st.write(f"❌ Incorrect: {st.session_state.answered - st.session_state.score}")
        st.write(f"📈 Accuracy: {accuracy:.2f}%")

        fig, ax = plt.subplots()
        ax.bar(["Correct", "Incorrect"], [st.session_state.score, st.session_state.answered - st.session_state.score])
        ax.set_ylabel("Count")
        ax.set_title("Quiz Performance")
        st.pyplot(fig)
    else:
        st.info("⚠️ No quiz attempts yet.")
