import streamlit as st

from services.quiz_generator import generate_quiz, insert_score
from services.rag_tutor import answer_question
from services.track_progress import get_level, get_latest_score
from services.upld_embed_store import Upld_embed_store
from services.study_planner import generate_study_plan

st.title("🎓 Smart Study Buddy")

option = st.sidebar.selectbox(
    "Choose",
    [
        "Upld Embed And Store",
        "Quiz",
        "Ask Tutor",
        "Track_Progress",
        "Create_Study_Schedule"
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
    # Keep quiz data and calculated scores persistent across button interactions
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "calculated_score" not in st.session_state:
        st.session_state.calculated_score = None
    if "current_subject" not in st.session_state:
        st.session_state.current_subject = "Math"

    topic = st.text_input("Topic" )

    if st.button("Generate Quiz" ):
        with st.spinner("Searching document context and preparing your test..."):
            st.session_state.questions = generate_quiz(topic)
            st.session_state.current_subject = topic
            st.session_state.calculated_score = None  # Reset score on new generation


    if st.session_state.questions:
        user_choices = {}
    
    # 1. Standard Interactive Form to display questions and fetch choices
    with st.form("quiz_evaluation_form"):
        for i, q in enumerate(st.session_state.questions):
            st.markdown(f"### Q{i+1}: {q['question']}")
            user_choices[i] = st.radio("Choose an option:", options=q["options"], key=f"quest_{i}")
            st.write("---")
            
        evaluate_click = st.form_submit_button("Grade Quiz Responses")
        
        if evaluate_click:
            correct_tally = 0
            for i, q in enumerate(st.session_state.questions):
                if user_choices[i] == q["answer"]:
                    correct_tally += 1
                    st.success(f"✅ Q{i+1} Correct!")
                else:
                    st.error(f"❌ Q{i+1} Wrong. Correct choice: {q['answer']}")
                st.info(f"ℹ️ *Explanation:* {q['explanation']}")
            
            st.session_state.calculated_score = correct_tally
            st.metric(label="Calculated Performance", value=f"{correct_tally} / 10")

    # 2. SEPARATE SUBMISSION BLOCK: Shown only after the quiz has been graded!
    if st.session_state.calculated_score is not None:
        st.write("---")
        st.subheader("💾 Lock in your Score")
        
        with st.form("score_save_form", clear_on_submit=True):
            student_name = st.text_input("Your Full Name")
            student_email = st.text_input("Your Email Address")
            
            # This is your requested 'Score_submit' element
            score_submit = st.form_submit_button("Submit Score to Database")
            
            if score_submit:
                if not student_name.strip() or not student_email.strip():
                    st.warning("Please fill out both name and email fields before recording.")
                else:
                    success = insert_score(
                        name=student_name,
                        email=student_email,
                        score=st.session_state.calculated_score,
                        subject=st.session_state.current_subject
                    )
                    if success:
                        st.success(f"🎉 Success! {student_name}'s score of {st.session_state.calculated_score}/10 saved.")
                    else:
                        st.error("Could not write record to database table. Check your logs.")

if option == "Ask Tutor":
    question = st.text_area("Ask Question")

    if st.button("Ask"):
        answer = answer_question(question, db_path="doc_index")
        st.write(answer)


if option == "Track_Progress":
    st.subheader("📊 Track Your Progress")
    st.write("This section allows you to view your quiz performance and mastery level.")

    # 1. Fetch live data from the SQLite database
    current_quiz_score, current_subject = get_latest_score()

    # 2. Check if records actually exist
    if current_quiz_score is not None:
        st.info(f"📚 **Latest Topic Attempted:** {current_subject}")

        # Display performance metrics side-by-side
        col1, col2 = st.columns(2)

        with col1:
            st.metric(label="Latest Quiz Score", value=f"{current_quiz_score} / 10")

        with col2:
            # Safely calculate mastery percentage assuming a 10-question quiz base
            mastery_percentage = current_quiz_score * 10
            mastery_level = get_level(mastery_percentage)
            st.metric(label="Mastery Level", value=mastery_level)
    else:
        # Fallback UI if the database table is completely blank
        st.warning(
            "No quiz records found yet! Head over to the Quiz section to take your first test."
        )

if option == "Create_Study_Schedule":
    st.subheader("📊 Check your Study Schedule")
    st.write("This section shows your Study Schedule.")

    # 3. User Inputs (Placed neatly in a sidebar)
    with st.sidebar:
        st.header("⚡ Input Your Details")
    
        # Days left for the exam (Integer input)
        exam_days = st.number_input("Days until exam:", min_value=1, max_value=365, value=30)
    
        # Hours available daily (Float/Slider input)
        hours_daily = st.slider("Available study hours per day:", min_value=1.0, max_value=16.0, value=4.0, step=0.5)
    
        # Weak topics (Text area input)
        weak_topics = st.text_area(
        "Weak Areas / Topics to focus on:", 
        placeholder="Polynomial Equation, Integration, Physics"
    )
    
    # Submit Button
    submit_button = st.button("Generate Study Plan", type="primary")

    # 4. Handling Action & Displaying Output
    if submit_button:
        if not weak_topics.strip():
            st.warning("⚠️ Please enter at least one weak topic to help customize your plan.")
        else:
            # Show a loading spinner while the AI processes
            with st.spinner("🧠 Analyzing your details and drafting your schedule..."):
                try:
                    # Call your function
                    study_plan_output = generate_study_plan(exam_days, hours_daily, weak_topics)
                    
                    # Display success message and output
                    st.success("✨ Your plan is ready!")
                    
                    # Container to visually separate the AI output
                    with st.container(border=True):
                        st.markdown(study_plan_output)
                        
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        # Default message before generation
        st.info("👈 Fill out your details in the sidebar and click **Generate Study Plan** to begin!")