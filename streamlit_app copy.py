import streamlit as st

from services.quiz_generator import generate_quiz
from services.rag_tutor import answer_question
from services.upld_embed_store import Upld_embed_store

st.title("🎓 Smart Study Buddy")

option = st.sidebar.selectbox(
    "Choose",
    [
        "Upld Embed And Store",
        "Quiz",
        "Ask Tutor",
        "Track_Progress",
        "Create_Study_Plan"
    ]
)

if option == "Upld Embed And Store":
    # Create an interactive file upload button
    uploaded_files = st.file_uploader(
        label="Select files to upload", 
        accept_multiple_files=True
    )

    #input = st.text_input("EmbedAndStore" )
    if st.button("Upld Embed And Store" ):
        Upld_embed_store(uploaded_files)

if option == "Quiz":
    topic = st.text_input("Topic" )

    if st.button("Generate Quiz" ):
        quiz = generate_quiz(topic)
        st.write(quiz)

if option == "Ask Tutor":

    question = st.text_area("Ask Question")

    if st.button("Ask"):
        answer = answer_question(question, db_path="doc_index")
        st.write(answer)