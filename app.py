import streamlit as st
import streamlit.components.v1 as components
import base64

from gemma_engine import ask_gemma
from prompts import (
    doubt_prompt,
    quiz_prompt,
    answer_check_prompt,
    study_plan_prompt,
)

st.set_page_config(
    page_title="ShikshaSetu AI",
    page_icon="logo.png",
    layout="wide",
)

# -----------------------------
# Video helper
# -----------------------------
def show_mascot_video(video_path, height=260):
    with open(video_path, "rb") as video_file:
        video_bytes = video_file.read()

    video_base64 = base64.b64encode(video_bytes).decode()

    components.html(
        f"""
        <video autoplay loop muted playsinline
            style="
                width: 100%;
                border-radius: 18px;
                background: #0E1117;
                object-fit: cover;
            ">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
        """,
        height=height,
    )


def is_error_response(text):
    if not isinstance(text, str):
        return True

    error_words = [
        "error",
        "failed",
        "connection failed",
        "not found",
        "timeout",
        "timed out",
        "no response",
        "model/api not found",
    ]

    clean = text.strip().lower()
    return any(word in clean for word in error_words)



# -----------------------------
MASCOT_VIDEOS = {
    "entry": "cat_entry.mp4",
    "idle": "cat_idle.mp4",
    "search": "cat_search.mp4",
    "success": "cat_success.mp4",
    "error": "cat_error.mp4",
}

if "mascot_state" not in st.session_state:
    st.session_state.mascot_state = "entry"

if "last_page" not in st.session_state:
    st.session_state.last_page = None


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.image("logo.png", width=110)
st.sidebar.title("ShikshaSetu AI")
st.sidebar.markdown(
    """
    <p style='color: gray; font-size: 14px;'>
    Learn smarter with Gemma 4
    </p>
    """,
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "Choose Feature",
    [
        "Ask a Doubt ❓",
        "Generate Quiz 📝",
        "Check My Answer ✅",
        "Make Study Plan 📅",
        "About Project ℹ️",
    ],
)

language = st.sidebar.selectbox(
    "Language",
    ["Hinglish", "Hindi", "English"],
)

level = st.sidebar.selectbox(
    "Student Level",
    ["Beginner", "School Student", "SSC Aspirant", "College Student"],
)

# When user changes page, return mascot to idle.
if st.session_state.last_page is None:
    st.session_state.last_page = page
elif st.session_state.last_page != page:
    st.session_state.mascot_state = "idle"
    st.session_state.last_page = page


# -----------------------------
# Cat message logic
# -----------------------------
if page == "Ask a Doubt ❓":
    cat_caption = "I can help you find simple answers."
    cat_emoji = "🔍"
elif page == "Generate Quiz 📝":
    cat_caption = "Let me create smart practice questions."
    cat_emoji = "📝"
elif page == "Check My Answer ✅":
    cat_caption = "I will check your answer like a tutor."
    cat_emoji = "✅"
elif page == "Make Study Plan 📅":
    cat_caption = "I can build your study roadmap."
    cat_emoji = "📅"
else:
    cat_caption = "Learn smarter with ShikshaSetu AI."
    cat_emoji = "💡"


def get_mascot_video():
    state = st.session_state.get("mascot_state", "idle")
    return MASCOT_VIDEOS.get(state, MASCOT_VIDEOS["idle"])


def render_mascot(video_box, caption_box, video_path=None, emoji=None, caption=None):
    video_path = video_path or get_mascot_video()
    emoji = emoji or cat_emoji
    caption = caption or cat_caption

    with video_box.container():
        show_mascot_video(video_path, height=260)

    with caption_box.container():
        st.markdown(
            f"""
            <div style="
                padding: 10px;
                border-radius: 14px;
                background: #111827;
                border: 1px solid #334155;
                text-align: center;
                margin-top: -35px;
            ">
                <b>{emoji} AI Study Cat</b><br>
                <span style="font-size: 14px; color: #cbd5e1;">{caption}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------
# Header with logo + cat
# -----------------------------
top_left, top_right = st.columns([3.2, 1.2], vertical_alignment="center")

with top_left:
    header_logo, header_text = st.columns([0.6, 5], vertical_alignment="center")

    with header_logo:
        st.image("logo.png", width=110)

    with header_text:
        st.markdown(
            "<h1 style='margin-bottom: 0;'>ShikshaSetu AI</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='margin-top: 4px;'>Gemma-powered Hindi/Hinglish AI Tutor for Rural Learners</h3>",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="
            padding: 18px;
            border-radius: 16px;
            background: linear-gradient(90deg, #102a43, #0b3d2e);
            border: 1px solid #2e7d32;
            margin-top: 12px;
            margin-bottom: 20px;
        ">
            <h3 style="margin-bottom: 8px;">🎓 Future of Education Project</h3>
            <p style="font-size: 16px;">
            ShikshaSetu AI helps rural and low-internet learners understand topics,
            generate quizzes, check answers, and build personalized study plans in
            Hindi, Hinglish, and English.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_right:
    mascot_video_box = st.empty()
    mascot_caption_box = st.empty()

render_mascot(mascot_video_box, mascot_caption_box)


# -----------------------------
# Feature cards
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info("❓ **Ask Doubts**\n\nSimple explanations with exam tips.")

with c2:
    st.success("📝 **Generate Quiz**\n\nMCQs with answers and explanations.")

with c3:
    st.warning("✅ **Check Answer**\n\nScore, mistakes, and improved answer.")

with c4:
    st.error("📅 **Study Plan**\n\nPersonalized day-wise preparation.")


def run_gemma_with_mascot(prompt, spinner_text, success_text):
    st.session_state.mascot_state = "search"
    render_mascot(
        mascot_video_box,
        mascot_caption_box,
        MASCOT_VIDEOS["search"],
        "🔎",
        "Searching the best answer for you...",
    )

    try:
        with st.spinner(spinner_text):
            response = ask_gemma(prompt)

        if is_error_response(response):
            st.session_state.mascot_state = "error"
            render_mascot(
                mascot_video_box,
                mascot_caption_box,
                MASCOT_VIDEOS["error"],
                "⚠️",
                "Something went wrong. Please try again.",
            )
            st.error("Model response issue detected.")
            st.markdown(response)
            return

        st.session_state.mascot_state = "success"
        render_mascot(
            mascot_video_box,
            mascot_caption_box,
            MASCOT_VIDEOS["success"],
            "✅",
            "Done! Your answer is ready.",
        )

        st.success(success_text)
        st.markdown(response)

    except Exception as e:
        st.session_state.mascot_state = "error"
        render_mascot(
            mascot_video_box,
            mascot_caption_box,
            MASCOT_VIDEOS["error"],
            "⚠️",
            "Something went wrong. Please try again.",
        )
        st.error(f"Error: {e}")


# -----------------------------
# Pages
# -----------------------------
if page == "Ask a Doubt ❓":
    st.header("❓ Ask a Doubt")

    question = st.text_area(
        "Apna doubt/question likho:",
        placeholder="Example: Buddhism aur Jainism me difference batao",
        height=150,
    )

    if st.button("✨ Explain My Doubt"):
        if question.strip():
            prompt = doubt_prompt(question, level, language)
            run_gemma_with_mascot(
                prompt,
                "ShikshaSetu AI answer bana raha hai...",
                "Answer ready ✅",
            )
        else:
            st.session_state.mascot_state = "error"
            render_mascot(
                mascot_video_box,
                mascot_caption_box,
                MASCOT_VIDEOS["error"],
                "⚠️",
                "Please write a question first.",
            )
            st.warning("Pehle question likho.")

elif page == "Generate Quiz 📝":
    st.header("📝 Generate Quiz")

    topic = st.text_input(
        "Topic likho:",
        placeholder="Example: Indus Valley Civilization",
    )

    if st.button("📝 Create Quiz"):
        if topic.strip():
            prompt = quiz_prompt(topic, level, language)
            run_gemma_with_mascot(
                prompt,
                "Quiz generate ho raha hai...",
                "Quiz ready ✅",
            )
        else:
            st.session_state.mascot_state = "error"
            render_mascot(
                mascot_video_box,
                mascot_caption_box,
                MASCOT_VIDEOS["error"],
                "⚠️",
                "Please write a topic first.",
            )
            st.warning("Pehle topic likho.")

elif page == "Check My Answer ✅":
    st.header("✅ Check My Answer")

    question = st.text_area(
        "Question:",
        placeholder="Example: Harappan Civilization ki main features kya thi?",
        height=120,
    )

    student_answer = st.text_area(
        "Tumhara answer:",
        placeholder="Example: Harappan civilization had planned cities, drainage system, trade and seals.",
        height=160,
    )

    if st.button("✅ Evaluate My Answer"):
        if question.strip() and student_answer.strip():
            prompt = answer_check_prompt(question, student_answer, language)
            run_gemma_with_mascot(
                prompt,
                "Answer evaluate ho raha hai...",
                "Evaluation ready ✅",
            )
        else:
            st.session_state.mascot_state = "error"
            render_mascot(
                mascot_video_box,
                mascot_caption_box,
                MASCOT_VIDEOS["error"],
                "⚠️",
                "Please write both question and answer.",
            )
            st.warning("Question aur answer dono likho.")

elif page == "Make Study Plan 📅":
    st.header("📅 Make Study Plan")

    goal = st.text_input(
        "Goal likho:",
        placeholder="Example: SSC CGL GK 30 din me complete karna hai",
    )

    days = st.number_input(
        "Kitne din available hain?",
        min_value=1,
        max_value=180,
        value=30,
    )

    if st.button("📅 Build My Study Plan"):
        if goal.strip():
            prompt = study_plan_prompt(goal, days, language)
            run_gemma_with_mascot(
                prompt,
                "Study plan ban raha hai...",
                "Study plan ready ✅",
            )
        else:
            st.session_state.mascot_state = "error"
            render_mascot(
                mascot_video_box,
                mascot_caption_box,
                MASCOT_VIDEOS["error"],
                "⚠️",
                "Please write a study goal first.",
            )
            st.warning("Pehle goal likho.")

elif page == "About Project ℹ️":
    st.header("ℹ️ About ShikshaSetu AI")

    st.markdown(
        """
        ## Project: ShikshaSetu AI

        **Track:** Future of Education

        ShikshaSetu AI is a Gemma-powered tutor designed for rural and low-internet learners.

        ### Problem
        Many students face:
        - Weak internet access
        - Expensive coaching
        - English language barrier
        - Lack of personal doubt-solving support

        ### Solution
        ShikshaSetu AI helps students with:
        - Simple Hindi/Hinglish explanations
        - Quiz generation
        - Answer evaluation
        - Personalized study planning

        ### How Gemma is Used
        Gemma is used as the core reasoning and language model for:
        - Explaining concepts
        - Generating quizzes
        - Evaluating answers
        - Creating study plans

        ### Impact
        This project supports accessible education for students who cannot depend on expensive coaching or strong internet.
        """
    )
