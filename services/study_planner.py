from services.gemini_service import ask_gemini


def generate_study_plan(
        exam_days,
        hours_daily,
        weak_topics):

    prompt = f"""
    Create a study schedule.

    Exam in: {exam_days} days

    Available Hours:
    {hours_daily}

    Weak Areas:
    {weak_topics}

    Generate daily plan.
    """

    return ask_gemini(prompt)


# Mock function for ask_gemini just to make the snippet executable
#def ask_gemini(prompt):
#    return f"### 📅 Your Custom Study Plan\nHere is your plan based on your inputs:\n\n* **Day 1-2:** Focus heavily on your weak topics: *{prompt.split('Weak Areas:')[1].split('Generate')[0].strip()}*.\n* **Day 3:** Review and practice tests."