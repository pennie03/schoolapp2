import streamlit as st
import json
import os
from datetime import date, datetime, timedelta


# =========================================================
# page setup
# =========================================================

st.set_page_config(
    page_title="learnloop",
    page_icon="📚",
    layout="wide",
)

# =========================================================
# LEARNLOOP LOGO
# =========================================================

LOGO_FILE = "1000099042.png"

# =========================================================
# data
# =========================================================

DATA_FILE = "studyhub_data.json"


DEFAULT_DATA = {
    "student_name": "",
    "grade": "grade 9",
    "subjects": ["math", "science", "english"],
    "goals": [],
    "study_time": 30,
    "tasks": [],
    "test_history": [],
    "streak": {
        "current": 0,
        "longest": 0,
        "last_active": ""
    },
    "theme": "light",
}


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                loaded = json.load(file)

            for key, value in DEFAULT_DATA.items():
                if key not in loaded:
                    loaded[key] = value.copy() if isinstance(value, dict) else (
                        value.copy() if isinstance(value, list) else value
                    )

            loaded.setdefault("streak", {})
            loaded["streak"].setdefault("current", 0)
            loaded["streak"].setdefault("longest", 0)
            loaded["streak"].setdefault("last_active", "")

            loaded.setdefault("test_history", [])
            loaded.setdefault("tasks", [])
            loaded.setdefault("subjects", DEFAULT_DATA["subjects"].copy())
            loaded.setdefault("goals", [])

            return loaded

        except Exception:
            return json.loads(json.dumps(DEFAULT_DATA))

    return json.loads(json.dumps(DEFAULT_DATA))


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


if "data" not in st.session_state:
    st.session_state.data = load_data()


data = st.session_state.data


# =========================================================
# theme
# =========================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = data.get("theme", "light") == "dark"


dark = st.session_state.dark_mode


if dark:
    COLORS = {
        "bg": "#202629",
        "sidebar": "#293438",
        "card": "#2A3235",
        "card2": "#313B3E",
        "text": "#F1F0EA",
        "muted": "#B7C0C0",
        "border": "#465357",
        "button": "#B9ADCF",
        "button_hover": "#C9BEDB",
        "input": "#2B3336",
        "progress_bg": "#3C484B",
        "accent": "#D2C7E4",
    }
else:
    COLORS = {
        "bg": "#FDFCFB",
        "sidebar": "#D2E5E6",
        "card": "#FFFFFF",
        "card2": "#F4F7F7",
        "text": "#465454",
        "muted": "#A2A8A8",
        "border": "#DDE3E3",
        "button": "#C7BDD9",
        "button_hover": "#B8ACCE",
        "input": "#FFFFFF",
        "progress_bg": "#E3EAEA",
        "accent": "#B8ACCE",
    }


st.markdown(
    f"""
<style>

.stApp {{
    background-color: {COLORS["bg"]};
    color: {COLORS["text"]};
}}

.main .block-container {{
    padding-top: 2rem;
    padding-left: 4rem;
    padding-right: 4rem;
    max-width: none;
    width: 100%;
}}

h1, h2, h3, h4, h5, h6,
p, label, .stMarkdown,
.stButton button, .stTextInput input,
.stTextArea textarea, .stSelectbox,
.stSlider, .stCheckbox, .stRadio,
.stNumberInput input {{
    font-family: Georgia, serif !important;
}}

h1, h2, h3, h4, h5, h6 {{
    color: {COLORS["text"]} !important;
}}

h1 {{
    font-size: 2.6rem !important;
}}

h2 {{
    font-size: 2.1rem !important;
}}

h3 {{
    font-size: 1.7rem !important;
}}

p, label, .stMarkdown {{
    color: {COLORS["text"]} !important;
}}

section[data-testid="stSidebar"] {{
    background-color: {COLORS["sidebar"]} !important;
    border-right: 1px solid {COLORS["border"]} !important;
    min-width: 245px;
    max-width: 270px;
}}

section[data-testid="stSidebar"] > div {{
    background-color: {COLORS["sidebar"]} !important;
}}

section[data-testid="stSidebar"] h1 {{
    color: {COLORS["text"]} !important;
    font-family: Georgia, serif !important;
    font-size: 1.35rem !important;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] {{
    gap: 0.5rem;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label {{
    display: block;
    padding: 0.8rem 0.9rem !important;
    margin: 0.15rem 0;
    border-radius: 12px;
    color: {COLORS["text"]} !important;
    font-family: Georgia, serif !important;
    font-size: 1.08rem !important;
    background-color: transparent !important;
    cursor: pointer;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
    background-color: rgba(255,255,255,0.18) !important;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
    background-color: rgba(255,255,255,0.24) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}}

.stButton > button {{
    background-color: {COLORS["button"]} !important;
    color: #424C4F !important;
    border: 1px solid {COLORS["accent"]} !important;
    border-radius: 12px !important;
    font-family: Georgia, serif !important;
    font-size: 1rem !important;
    padding: 0.6rem 1.3rem !important;
}}

.stButton > button:hover {{
    background-color: {COLORS["button_hover"]} !important;
    transform: translateY(-1px);
}}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {{
    border-radius: 10px !important;
    border: 1px solid {COLORS["border"]} !important;
    background-color: {COLORS["input"]} !important;
    color: {COLORS["text"]} !important;
}}

div[data-baseweb="select"] > div {{
    border-radius: 10px !important;
    border-color: {COLORS["border"]} !important;
    background-color: {COLORS["input"]} !important;
    color: {COLORS["text"]} !important;
}}

div[data-testid="stMetric-container"] {{
    background-color: {COLORS["card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 16px;
    padding: 1.2rem;
    box-shadow: 0 3px 12px rgba(0,0,0,0.07);
}}

div[data-testid="stMetric-container"] label {{
    color: {COLORS["muted"]} !important;
}}

div[data-testid="stMetric-container"] [data-testid="stMetricValue"] {{
    color: {COLORS["text"]} !important;
}}

.stProgress > div > div > div > div {{
    background-color: {COLORS["text"]} !important;
}}

.stProgress > div > div {{
    background-color: {COLORS["progress_bg"]} !important;
}}

hr {{
    border-color: {COLORS["border"]} !important;
}}

.study-card {{
    background: {COLORS["card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 18px;
    padding: 1.4rem;
    margin: 0.5rem 0 1rem 0;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
}}

.focus-card {{
    background: {COLORS["card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 24px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.09);
}}

.timer {{
    font-family: Georgia, serif;
    font-size: 5rem;
    font-weight: bold;
    letter-spacing: 0.04em;
    color: {COLORS["text"]};
    margin: 0.5rem 0;
}}

.goal-box {{
    background: {COLORS["card2"]};
    border-left: 5px solid {COLORS["accent"]};
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
}}

.focus-mode-selector {{
    background: {COLORS["card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 20px;
    padding: 1.4rem;
    text-align: center;
    height: 100%;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}}

.focus-mode-selector h3 {{
    margin-bottom: 0.4rem;
}}

.focus-mode-selector p {{
    color: {COLORS["muted"]} !important;
}}

.focus-overlay {{
    position: fixed;
    inset: 0;
    background: rgba(25, 30, 32, 0.74);
    z-index: 999999;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}}

.focus-overlay-card {{
    width: min(520px, 90vw);
    padding: 38px;
    border-radius: 26px;
    background: {COLORS["card"]};
    border: 1px solid {COLORS["border"]};
    text-align: center;
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
    font-family: Georgia, serif;
}}

.focus-overlay-icon {{
    font-size: 48px;
    margin-bottom: 10px;
}}

.focus-overlay-title {{
    color: {COLORS["text"]};
    font-family: Georgia, serif;
    margin-bottom: 12px;
}}

.focus-overlay-text {{
    color: {COLORS["text"]};
    font-size: 18px;
    line-height: 1.5;
}}

.focus-overlay-button {{
    margin-top: 15px;
    padding: 12px 24px;
    border: 0;
    border-radius: 12px;
    background: {COLORS["button"]};
    color: #424C4F;
    font-family: Georgia, serif;
    cursor: pointer;
    font-size: 16px;
}}

.focus-overlay-button:hover {{
    background: {COLORS["button_hover"]};
}}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# helpers
# =========================================================


def update_streak(data):
    today = date.today()

    streak = data.setdefault(
        "streak",
        {"current": 0, "longest": 0, "last_active": ""},
    )

    last_active = streak.get("last_active", "")

    if not last_active:
        streak["current"] = 1
        streak["longest"] = max(streak.get("longest", 0), 1)
        streak["last_active"] = str(today)

    else:
        try:
            last_date = date.fromisoformat(last_active)
            days_since = (today - last_date).days
        except Exception:
            days_since = 999

        if days_since == 0:
            return

        if days_since == 1:
            streak["current"] = streak.get("current", 0) + 1
        else:
            streak["current"] = 1

        streak["longest"] = max(
            streak.get("longest", 0),
            streak["current"],
        )

        streak["last_active"] = str(today)

    save_data(data)


def get_unfinished_tasks(data):
    return [
        task for task in data.get("tasks", [])
        if not task.get("completed", False)
    ]


def task_due_days(task):
    try:
        return (
            date.fromisoformat(task.get("due", str(date.today())))
            - date.today()
        ).days
    except Exception:
        return 999


def get_recommended_tasks(data, limit=3):
    tasks = get_unfinished_tasks(data)
    return sorted(tasks, key=task_due_days)[:limit]


def call_gemini(prompt):
    from google import genai

    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        raise RuntimeError(
            "learno is not available at the moment."
        )

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text


def clean_json_response(text):
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        lines = [
            line for line in lines
            if not line.strip().startswith("```")
        ]
        text = "\n".join(lines).strip()

    return json.loads(text)


def grade_label(percent):
    if percent >= 90:
        return "excellent"
    if percent >= 80:
        return "strong"
    if percent >= 70:
        return "good"
    if percent >= 60:
        return "developing"
    return "needs more practice"


# =========================================================
# study tips
# =========================================================


STUDY_TIPS = {
    "🧠 memory": [
        ("teach it out loud", "explain the idea out loud as if you were teaching someone else."),
        ("use active recall", "close your notes and try to remember the important ideas yourself."),
        ("connect new ideas", "connect something you're learning to something you already know."),
        ("make your own examples", "create your own example after learning a concept."),
    ],
    "📚 studying": [
        ("start with one small task", "choose one small task instead of thinking about everything at once."),
        ("study in chunks", "break a large study session into smaller sections with clear goals."),
        ("switch up your methods", "combine notes, practice questions, explaining, and mistake review."),
        ("review before you forget", "short reviews spread across several days can help reinforce learning."),
    ],
    "📝 tests": [
        ("practice without your notes", "try practice questions before checking your notes."),
        ("learn from mistakes", "figure out why an answer was wrong instead of only memorizing the correct one."),
        ("read questions carefully", "make sure you know exactly what a question is asking."),
        ("practice the tricky parts", "spend extra time on concepts you regularly find difficult."),
    ],
    "🎯 focus": [
        ("remove one distraction", "remove one thing that usually pulls your attention away."),
        ("choose a clear goal", "use a specific goal such as 'finish five practice questions.'"),
        ("keep your workspace simple", "keep only the materials you need in front of you."),
        ("take intentional breaks", "step away from your work during breaks and return refreshed."),
    ],
    "🌙 rest": [
        ("sleep is part of studying", "rest gives your brain time to process what you've learned."),
        ("don't ignore tiredness", "if you're exhausted, rest may be more useful than forcing more work."),
        ("give yourself downtime", "make room for hobbies, friends, movement, and relaxing."),
        ("plan tomorrow before stopping", "write down your next task before ending a study session."),
    ],
}


# =========================================================
# sidebar
# =========================================================


# LearnLoop logo
if os.path.exists(LOGO_FILE):
    st.sidebar.image(
        LOGO_FILE,
        use_container_width=True
    )


page = st.sidebar.radio(
    "navigate",
    [
        "🏠 dashboard",
        "👤 profile",
        "📝 tasks",
        "💡 study tips",
        "📝 tests",
        "🤖 ai helper",
    ],
)


st.sidebar.divider()


new_dark = st.sidebar.toggle(
    "🌙 dark mode",
    value=dark,
)


if new_dark != st.session_state.dark_mode:
    st.session_state.dark_mode = new_dark
    data["theme"] = "dark" if new_dark else "light"
    save_data(data)
    st.rerun()


# =========================================================
# header
# =========================================================


st.title("learnloop")


if data.get("student_name"):
    st.write(
        f"welcome back, {data['student_name']}! "
        "let's make studying a little easier today. 🌷"
    )
else:
    st.write("your personalized learning companion.")


# =========================================================
# dashboard
# =========================================================


if page == "🏠 dashboard":

    st.header("✨ your dashboard")

    tasks = data.get("tasks", [])
    subjects = data.get("subjects", [])

    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks if task.get("completed", False)
    )

    overall_progress = (
        completed_tasks / total_tasks
        if total_tasks else 0
    )

    streak = data.get("streak", {})
    current_streak = streak.get("current", 0)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "overall progress",
            f"{int(overall_progress * 100)}%",
        )

    with col2:
        st.metric(
            "tasks completed",
            f"{completed_tasks}/{total_tasks}",
        )

    with col3:
        st.metric(
            "study time available",
            f"{data.get('study_time', 30)} min",
        )

    with col4:
        st.metric(
            "🔥 study streak",
            f"{current_streak} days",
        )

    st.divider()

    longest = streak.get("longest", 0)

    if current_streak == 0:
        streak_message = "complete a study action to start your streak. 🌱"
    elif current_streak < 7:
        streak_message = f"you're on a {current_streak}-day streak! keep building the habit."
    elif current_streak < 14:
        streak_message = f"🌟 {current_streak} days in a row! you're building strong momentum."
    else:
        streak_message = f"🏆 {current_streak} days! that's some serious consistency."

    st.markdown(
        f"""
        <div class="study-card">
            <h3>🔥 your study streak</h3>
            <p>{streak_message}</p>
            <p style="color:{COLORS["muted"]} !important;">
                longest streak: {longest} days
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("🌱 your focus today")

    unfinished = get_unfinished_tasks(data)

    if unfinished:
        recommended = get_recommended_tasks(data, 1)[0]
        days = task_due_days(recommended)

        if days < 0:
            urgency = "🚨 overdue"
        elif days == 0:
            urgency = "🔥 due today"
        elif days == 1:
            urgency = "⏰ due tomorrow"
        else:
            urgency = f"📅 due in {days} days"

        st.info(
            f"### 📖 {recommended.get('title', 'untitled task')}\n\n"
            f"subject: {recommended.get('subject', 'general').lower()}\n\n"
            f"{urgency}\n\n"
            f"you have {data.get('study_time', 30)} minutes available today."
        )
    else:
        st.success(
            "🎉 you're all caught up! there are no unfinished tasks right now."
        )

    st.divider()

    st.subheader("📚 your subjects")

    if subjects:
        for start in range(0, len(subjects), 3):
            row = subjects[start:start + 3]
            cols = st.columns(len(row))

            for i, subject in enumerate(row):
                subject_tasks = [
                    task for task in tasks
                    if task.get("subject", "").lower() == subject.lower()
                ]

                total = len(subject_tasks)

                complete = sum(
                    1 for task in subject_tasks
                    if task.get("completed", False)
                )

                progress = complete / total if total else 0

                with cols[i]:
                    st.markdown(f"### {subject.lower()}")
                    st.progress(progress)
                    st.write(f"{int(progress * 100)}% complete")
                    st.caption(
                        f"{complete} of {total} tasks completed"
                        if total else "no tasks yet"
                    )
    else:
        st.info("add some subjects in your profile.")

    st.divider()

    st.subheader("💭 a little note")

    if overall_progress == 0:
        st.write("you've got a blank slate. add a task and let's get started. 🌱")
    elif overall_progress < 0.5:
        st.write("you're building momentum. every completed task counts. ✨")
    elif overall_progress < 1:
        st.write("you're more than halfway there! keep going. 🌷")
    else:
        st.write("you finished everything! take a well-earned break. 🎉")


# =========================================================
# profile
# =========================================================


elif page == "👤 profile":

    st.header("👤 my study profile")

    st.write(
        "personalize learnloop so your dashboard can give you better recommendations. 🌱"
    )

    st.divider()

    name = st.text_input(
        "what's your name?",
        value=data.get("student_name", ""),
    )

    subjects_text = st.text_input(
        "enter your subjects, separated by commas",
        value=", ".join(data.get("subjects", [])),
    )

    grade_options = [
        "grade 6",
        "grade 7",
        "grade 8",
        "grade 9",
        "grade 10",
        "grade 11",
        "grade 12",
    ]

    current_grade = data.get("grade", "grade 9")

    if current_grade not in grade_options:
        current_grade = "grade 9"

    grade = st.selectbox(
        "what grade are you in?",
        grade_options,
        index=grade_options.index(current_grade),
    )

    goal_options = [
        "staying organized",
        "improving my grades",
        "preparing for tests",
        "finishing assignments",
        "building better study habits",
    ]

    current_goal = (
        data.get("goals", ["staying organized"])[0]
        if data.get("goals")
        else "staying organized"
    )

    if current_goal not in goal_options:
        current_goal = "staying organized"

    goal = st.selectbox(
        "what are you trying to accomplish?",
        goal_options,
        index=goal_options.index(current_goal),
    )

    study_time = st.slider(
        "how many minutes can you study today?",
        min_value=10,
        max_value=180,
        value=int(data.get("study_time", 30)),
        step=10,
    )

    if st.button("💾 save profile"):

        if subjects_text.strip():

            data["student_name"] = name.strip()
            data["grade"] = grade

            data["subjects"] = [
                s.strip().lower()
                for s in subjects_text.split(",")
                if s.strip()
            ]

            data["goals"] = [goal]
            data["study_time"] = study_time

            save_data(data)

            st.success("profile saved! ✨")
            st.rerun()

        else:
            st.warning("please enter at least one subject.")


# =========================================================
# tasks
# =========================================================


elif page == "📝 tasks":

    st.header("📝 tasks")

    st.subheader("➕ add a task")

    title = st.text_input(
        "task name",
        placeholder="example: finish algebra worksheet",
    )

    subject = st.selectbox(
        "subject",
        data.get("subjects", []) or ["general"],
    )

    due_date = st.date_input(
        "due date",
        value=date.today(),
    )

    if st.button("➕ add task"):

        if title.strip():

            data.setdefault("tasks", []).append({
                "title": title.strip(),
                "subject": subject,
                "due": str(due_date),
                "completed": False,
            })

            save_data(data)

            st.success("task added! 🎉")
            st.rerun()

        else:
            st.warning("please enter a task name.")

    st.divider()

    st.subheader("📋 your tasks")

    if not data.get("tasks"):

        st.info("no tasks yet. add your first task above!")

    else:

        for i, task in enumerate(data["tasks"]):

            col1, col2 = st.columns([5, 1])

            with col1:

                completed = st.checkbox(
                    f"{task.get('title', 'untitled')} • "
                    f"{task.get('subject', 'general')} • "
                    f"due {task.get('due', '')}",
                    value=task.get("completed", False),
                    key=f"task_checkbox_{i}",
                )

                if completed != task.get("completed", False):

                    task["completed"] = completed
                    save_data(data)

                    if completed:
                        update_streak(data)

                    st.rerun()

            with col2:

                if st.button(
                    "🗑️",
                    key=f"delete_task_{i}",
                ):

                    data["tasks"].pop(i)
                    save_data(data)
                    st.rerun()


# =========================================================
# study tips
# =========================================================


elif page == "💡 study tips":

    st.header("💡 study tips")

    st.write(
        "small strategies that can make studying a little easier. 🌷"
    )

    all_tips = []

    for category, tips in STUDY_TIPS.items():

        for title, tip in tips:

            all_tips.append({
                "category": category,
                "title": title,
                "tip": tip,
            })

    st.subheader("✨ tip of the day")

    daily_tip = all_tips[
        date.today().toordinal() % len(all_tips)
    ]

    goal_text = (
        data.get("goals", ["building better study habits"])[0]
        if data.get("goals")
        else "building better study habits"
    )

    st.markdown(
        f"""
        <div class="study-card">
            <p style="color:{COLORS["muted"]} !important;">
                {daily_tip["category"]} • {data.get("grade", "grade 9")}
            </p>
            <h2>{daily_tip["title"]}</h2>
            <p>{daily_tip["tip"]}</p>
            <p style="color:{COLORS["muted"]} !important;">
                🎯 current goal: {goal_text}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("📚 explore study tips")

    selected_category = st.selectbox(
        "choose a category",
        list(STUDY_TIPS.keys()),
    )

    for title, tip in STUDY_TIPS[selected_category]:

        with st.container(border=True):

            st.markdown(f"### ✦ {title}")
            st.write(tip)

    st.subheader("🌷 make it work for you")

    st.info(
        f"you're currently working toward {goal_text} as a "
        f"{data.get('grade', 'grade 9')} student. "
        "pick one small strategy to try today."
    )


# =========================================================
# tests
# =========================================================


elif page == "📝 tests":

    st.header("📝 practice tests")

    st.write(
        "create a practice test, enter an existing grade, "
        "or let learnloop recommend what to practice next. 🌱"
    )

    # -----------------------------------------------------
    # grade analyzer
    # -----------------------------------------------------

    st.subheader("📊 analyze a grade")

    grade_format = st.radio(
        "how is your grade recorded?",
        ["percentage", "points"],
        horizontal=True,
    )

    if grade_format == "percentage":

        percentage_input = st.number_input(
            "enter your percentage",
            min_value=0.0,
            max_value=100.0,
            value=75.0,
            step=1.0,
        )

        calculated_percentage = percentage_input

    else:

        point_score = st.number_input(
            "points earned",
            min_value=0.0,
            value=18.0,
            step=1.0,
        )

        point_total = st.number_input(
            "points possible",
            min_value=1.0,
            value=25.0,
            step=1.0,
        )

        calculated_percentage = (
            point_score / point_total * 100
        )

    st.metric(
        "calculated grade",
        f"{calculated_percentage:.0f}%",
    )

    grade_topic = st.text_input(
        "what subject/topic was this grade for?",
        placeholder="example: grade 9 science - cells",
        key="grade_topic",
    )

    if st.button("🤖 analyze my grade"):

        if not grade_topic.strip():

            st.warning(
                "enter the subject or topic first."
            )

        else:

            prompt = f"""
you are learnloop, a friendly study assistant.

a student in {data.get("grade", "grade 9")} received
a grade of {calculated_percentage:.1f}% on:
{grade_topic}

analyze this result in a supportive, non-judgmental way.

return only valid json with this exact structure:

{{
    "summary": "short supportive analysis",
    "strength": "one thing the student is likely doing well",
    "next_step": "one useful next step",
    "recommended_test": {{
        "subject": "subject",
        "topic": "specific topic",
        "difficulty": "easy, medium, or challenging",
        "questions": 5,
        "reason": "why this test is recommended"
    }}
}}

do not make assumptions about the student's ability.
a grade is one result, not a measure of intelligence.
"""

            try:

                with st.spinner(
                    "learnloop is analyzing your grade... ✨"
                ):

                    result = clean_json_response(
                        call_gemini(prompt)
                    )

                st.session_state.grade_analysis = result
                st.session_state.grade_percentage = calculated_percentage

            except Exception as e:

                st.error(
                    "learnloop couldn't analyze the grade right now."
                )

                st.caption(str(e))


    if "grade_analysis" in st.session_state:

        result = st.session_state.grade_analysis
        percentage = st.session_state.grade_percentage

        st.divider()

        st.markdown(
            f"""
            <div class="study-card">
                <h2>🌷 your result: {percentage:.0f}%</h2>
                <p>{result.get("summary", "")}</p>
                <p>💪 strength: {result.get("strength", "")}</p>
                <p>🎯 next step: {result.get("next_step", "")}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        recommended = result.get(
            "recommended_test",
            {},
        )

        st.subheader("🎯 recommended test")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                f"""
                subject: {recommended.get("subject", "general")}

                topic: {recommended.get("topic", "review")}

                difficulty: {recommended.get("difficulty", "medium")}
                """
            )

        with col2:

            st.markdown(
                f"""
                questions: {recommended.get("questions", 5)}

                why: {recommended.get("reason", "more practice may help reinforce the topic.")}
                """
            )

        if st.button(
            "✨ generate my recommended test"
        ):

            st.session_state.recommended_test_settings = {
                "subject": recommended.get(
                    "subject",
                    "general",
                ),
                "topic": recommended.get(
                    "topic",
                    "",
                ),
                "difficulty": recommended.get(
                    "difficulty",
                    "medium",
                ),
                "questions": int(
                    recommended.get(
                        "questions",
                        5,
                    )
                ),
            }

            st.success(
                "recommended settings are ready below. 🌱"
            )

    st.divider()

    # -----------------------------------------------------
    # test generator
    # -----------------------------------------------------

    st.subheader("✨ create a practice test")

    recommended_settings = st.session_state.get(
        "recommended_test_settings",
        {},
    )

    subject_options = (
        data.get("subjects", [])
        or ["general"]
    )

    default_subject = recommended_settings.get(
        "subject",
        subject_options[0],
    )

    if default_subject not in subject_options:
        subject_options = subject_options + [
            default_subject
        ]

    subject = st.selectbox(
        "📚 choose a subject",
        subject_options,
        index=subject_options.index(
            default_subject
        ),
    )

    topic = st.text_input(
        "📖 what topic should the test cover?",
        value=recommended_settings.get(
            "topic",
            "",
        ),
        placeholder="example: quadratic equations",
    )

    difficulty_options = [
        "easy",
        "medium",
        "challenging",
    ]

    default_difficulty = recommended_settings.get(
        "difficulty",
        "medium",
    )

    if default_difficulty not in difficulty_options:
        default_difficulty = "medium"

    difficulty = st.selectbox(
        "🌱 difficulty",
        difficulty_options,
        index=difficulty_options.index(
            default_difficulty
        ),
    )

    default_questions = int(
        recommended_settings.get(
            "questions",
            5,
        )
    )

    default_questions = max(
        3,
        min(
            10,
            default_questions,
        ),
    )

    num_questions = st.slider(
        "📝 number of questions",
        min_value=3,
        max_value=10,
        value=default_questions,
    )

    if st.button(
        "✨ generate practice test"
    ):

        if not topic.strip():

            st.warning(
                "please enter a topic first."
            )

        else:

            prompt = f"""
you are learnloop's practice test generator.

create a practice test for a student.

subject: {subject}
grade level: {data.get("grade", "grade 9")}
topic: {topic}
difficulty: {difficulty}
number of questions: {num_questions}

return only valid json.

the json must have this exact structure:

{{
    "questions": [
        {{
            "question": "question text",
            "options": [
                "option a",
                "option b",
                "option c",
                "option d"
            ],
            "answer": 0,
            "explanation": "short explanation"
        }}
    ]
}}

rules:

- create exactly {num_questions} questions.
- every question must be appropriate for the grade level.
- each question has exactly 4 options.
- only one option is correct.
- the answer must be 0, 1, 2, or 3.
- easy tests basic understanding.
- medium tests understanding and application.
- challenging questions may require multiple steps.
- avoid trick questions.
"""

            try:

                with st.spinner(
                    "learnloop is creating your test... ✨"
                ):

                    test_data = clean_json_response(
                        call_gemini(prompt)
                    )

                test_data["subject"] = subject
                test_data["topic"] = topic
                test_data["difficulty"] = difficulty

                st.session_state.practice_test = test_data
                st.session_state.test_question = 0
                st.session_state.test_score = 0
                st.session_state.test_answered = False
                st.session_state.test_finished = False

                st.rerun()

            except Exception as e:

                st.error(
                    "something went wrong while creating the test."
                )

                st.caption(str(e))


    # -----------------------------------------------------
    # active test
    # -----------------------------------------------------

    if (
        "practice_test" in st.session_state
        and not st.session_state.get(
            "test_finished",
            False,
        )
    ):

        test = st.session_state.practice_test
        questions = test.get("questions", [])
        current = st.session_state.test_question

        if not questions:

            st.error(
                "this test didn't contain any questions."
            )

        else:

            question = questions[current]

            st.divider()

            st.progress(
                current / len(questions)
            )

            st.caption(
                f"question {current + 1} of {len(questions)}"
            )

            st.subheader(
                question["question"]
            )

            selected = st.radio(
                "choose an answer:",
                question["options"],
                key=f"answer_{current}",
            )

            selected_index = (
                question["options"].index(
                    selected
                )
            )

            if not st.session_state.test_answered:

                if st.button(
                    "✅ check answer",
                    key=f"check_{current}",
                ):

                    st.session_state.test_answered = True

                    if (
                        selected_index
                        == question["answer"]
                    ):

                        st.session_state.test_score += 1

                    st.rerun()

            else:

                correct_index = question["answer"]

                if selected_index == correct_index:

                    st.success(
                        "🎉 correct!"
                    )

                else:

                    st.error(
                        f"not quite! the correct answer was: "
                        f"{question['options'][correct_index]}"
                    )

                st.info(
                    f"💡 why: "
                    f"{question.get('explanation', '')}"
                )

                if current + 1 < len(questions):

                    if st.button(
                        "➡️ next question",
                        key=f"next_{current}",
                    ):

                        st.session_state.test_question += 1
                        st.session_state.test_answered = False
                        st.rerun()

                else:

                    if st.button(
                        "🏁 finish test",
                        key="finish_test",
                    ):

                        total = len(questions)
                        score = st.session_state.test_score

                        percentage = int(
                            (score / total) * 100
                        )

                        data.setdefault(
                            "test_history",
                            [],
                        ).append({
                            "subject": test.get(
                                "subject",
                                subject,
                            ),
                            "topic": test.get(
                                "topic",
                                topic,
                            ),
                            "score": score,
                            "total": total,
                            "percentage": percentage,
                            "difficulty": test.get(
                                "difficulty",
                                difficulty,
                            ),
                            "date": str(
                                date.today()
                            ),
                        })

                        update_streak(data)

                        st.session_state.test_finished = True

                        st.rerun()


    # -----------------------------------------------------
    # final score
    # -----------------------------------------------------

    if (
        "practice_test" in st.session_state
        and st.session_state.get(
            "test_finished",
            False,
        )
    ):

        test = st.session_state.practice_test

        total = len(
            test["questions"]
        )

        score = st.session_state.test_score

        percentage = int(
            (score / total) * 100
        )

        st.divider()

        st.header("🎉 test complete!")

        st.metric(
            "your score",
            f"{score}/{total}",
        )

        st.progress(
            percentage / 100
        )

        if percentage == 100:

            st.success(
                "perfect score! 🌟"
            )

        elif percentage >= 80:

            st.success(
                "great job! you're really getting the hang of this. 🌱"
            )

        elif percentage >= 60:

            st.info(
                "good effort! review the questions you missed and try again."
            )

        else:

            st.warning(
                "keep practicing! every attempt helps you learn."
            )

        if st.button(
            "🔄 create another test"
        ):

            for key in [
                "practice_test",
                "test_question",
                "test_score",
                "test_answered",
                "test_finished",
            ]:

                st.session_state.pop(
                    key,
                    None,
                )

            st.rerun()


    # -----------------------------------------------------
    # test history
    # -----------------------------------------------------

    st.divider()

    st.subheader("📊 your test history")

    history = data.get(
        "test_history",
        [],
    )

    if history:

        for result in reversed(history):

            percentage = result.get(
                "percentage",
                0,
            )

            st.markdown(
                f"### {result.get('subject', 'general').lower()} • "
                f"{result.get('topic', 'untitled')}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "score",
                    f"{result.get('score', 0)}/"
                    f"{result.get('total', 0)}",
                )

            with col2:

                st.metric(
                    "percentage",
                    f"{percentage}%",
                )

            with col3:

                st.write(
                    f"difficulty\n\n"
                    f"{result.get('difficulty', 'medium')}"
                )

            st.progress(
                percentage / 100
            )

            st.caption(
                result.get("date", "")
            )

            st.divider()

    else:

        st.info(
            "your completed practice tests will appear here. 🌱"
        )


# =========================================================
# ai helper
# =========================================================


elif page == "🤖 ai helper":

    st.header("🤖 lerno, the ai study helper")

    st.write(
        "ask lerno for explanations, study strategies, "
        "practice questions, or help understanding a topic."
    )

    question = st.text_area(
        "what do you need help with?",
        placeholder="example: explain photosynthesis in a simple way.",
        height=150,
    )

    if st.button(
        "✨ ask lerno"
    ):

        if question.strip():

            prompt = f"""
you are lerno, a friendly ai study assistant.

the student is in:
{data.get("grade", "grade 9")}

the student asked:

{question}

help the student understand the topic.

rules:

- explain things clearly and simply.
- adjust the explanation to the student's grade level.
- break difficult ideas into smaller steps.
- give examples when helpful.
- if this is homework, guide the student instead of simply giving the answer.
- encourage the student to think through the problem themselves.
- keep your response organized and easy to read.
"""

            try:

                with st.spinner(
                    "lerno is thinking... ✨"
                ):

                    response = call_gemini(
                        prompt
                    )

                st.divider()

                st.subheader(
                    "🌷 lerno's answer"
                )

                st.write(
                    response
                )

            except Exception as e:

                st.error(
                    "something went wrong while connecting to gemini."
                )

                st.caption(
                    str(e)
                )

        else:

            st.warning(
                "type a question first!"
            )
