import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CA Final Nov 2026 Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

div[data-testid="metric-container"] {
    background-color: #111827;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1f2937;
}

div[data-testid="metric-container"] label {
    color: white !important;
}

div[data-testid="metric-container"] div {
    color: white !important;
}

.stProgress > div > div > div > div {
    background-color: #3b82f6;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📌 CA Final Planner")

st.sidebar.markdown("""
### Exam Details
- Attempt: Nov 2026
- Exam Date: 2 Nov 2026

### Subjects
- FR
- AFM
- DT
- IDT
- Audit

### Goal
Complete lectures + revisions before Oct end.
""")

# =========================================================
# TITLE
# =========================================================

st.title("📚 CA Final Nov 2026 Preparation Dashboard")

st.markdown("""
Track your:
- Lecture Completion
- Revision Progress
- Mock Tests
- Daily Discipline
- Exam Readiness
""")

# =========================================================
# EXAM COUNTDOWN
# =========================================================

exam_date = datetime(2026, 11, 2)
today = datetime.today()

remaining_days = (exam_date - today).days

st.subheader("⏳ Exam Countdown")

col1, col2 = st.columns(2)

col1.metric(
    "Days Remaining",
    remaining_days
)

months_remaining = round(remaining_days / 30, 1)

col2.metric(
    "Months Remaining",
    months_remaining
)

# =========================================================
# SUBJECT DATA
# =========================================================

subjects = {
    "IDT": {
        "total": 110,
        "completed": 65
    },
    "DT": {
        "total": 200,
        "completed": 10
    },
    "FR": {
        "total": 200,
        "completed": 0
    },
    "AFM": {
        "total": 200,
        "completed": 0
    },
    "Audit": {
        "total": 110,
        "completed": 0
    }
}

# =========================================================
# CREATE DATAFRAME
# =========================================================

data = []

for subject, values in subjects.items():

    total = values["total"]
    completed = values["completed"]
    remaining = total - completed

    completion = round(
        (completed / total) * 100,
        2
    )

    data.append({
        "Subject": subject,
        "Total Hours": total,
        "Completed Hours": completed,
        "Remaining Hours": remaining,
        "Completion %": completion
    })

df = pd.DataFrame(data)

# =========================================================
# OVERALL METRICS
# =========================================================

total_hours = df["Total Hours"].sum()
completed_hours = df["Completed Hours"].sum()
remaining_hours = df["Remaining Hours"].sum()

overall_completion = round(
    (completed_hours / total_hours) * 100,
    2
)

st.subheader("📈 Overall Progress")

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Total Hours",
    total_hours
)

metric2.metric(
    "Completed",
    completed_hours
)

metric3.metric(
    "Remaining",
    remaining_hours
)

metric4.metric(
    "Completion %",
    f"{overall_completion}%"
)

st.progress(overall_completion / 100)

# =========================================================
# SUBJECT PROGRESS TABLE
# =========================================================

st.subheader("📋 Subject Wise Progress")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# CHARTS
# =========================================================

st.subheader("📊 Lecture Completion Chart")

fig = px.bar(
    df,
    x="Subject",
    y="Completion %",
    text="Completion %",
    title="Lecture Completion Percentage"
)

fig.update_traces(
    textposition="outside"
)

fig.update_layout(
    yaxis_range=[0, 100],
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# DAILY TARGETS
# =========================================================

st.subheader("🎯 Daily Target Calculator")

weeks_remaining = remaining_days // 7

daily_target = round(
    remaining_hours / remaining_days,
    2
)

weekly_target = round(
    remaining_hours / weeks_remaining,
    2
)

target1, target2 = st.columns(2)

target1.metric(
    "Daily Lecture Hours Needed",
    daily_target
)

target2.metric(
    "Weekly Lecture Hours Needed",
    weekly_target
)

# =========================================================
# MONTHLY TARGETS
# =========================================================

st.subheader("🗓️ Monthly Preparation Plan")

monthly_targets = pd.DataFrame({
    "Month": [
        "May 2026",
        "June 2026",
        "July 2026",
        "August 2026",
        "September 2026",
        "October 2026"
    ],
    "Target": [
        "Finish IDT + Strong DT Start",
        "Heavy DT + FR Progress",
        "Finish DT + Continue FR + Start AFM",
        "Complete All Lectures",
        "1st Full Revision",
        "Mocks + Final Revision"
    ]
})

st.table(monthly_targets)

# =========================================================
# DAILY STUDY SCHEDULE
# =========================================================

st.subheader("⏰ Ideal Daily Study Schedule")

schedule_df = pd.DataFrame({
    "Time": [
        "6:30 AM – 8:30 AM",
        "9:00 AM – 1:00 PM",
        "2:00 PM – 5:00 PM",
        "6:00 PM – 8:00 PM",
        "9:00 PM – 10:00 PM"
    ],
    "Task": [
        "Revision + Practice",
        "Main Lecture Block",
        "Second Lecture Block",
        "Question Practice / Self Study",
        "Audit / DT Revision"
    ]
})

st.table(schedule_df)

# =========================================================
# REVISION TRACKER
# =========================================================

st.subheader("🔁 Revision Tracker")

rev_col1, rev_col2 = st.columns(2)

revision_subject = rev_col1.selectbox(
    "Select Subject",
    list(subjects.keys())
)

revision_round = rev_col2.selectbox(
    "Revision Round",
    [
        "1st Revision",
        "2nd Revision",
        "Final Revision"
    ]
)

revision_status = st.checkbox(
    "Mark Revision Completed"
)

if revision_status:

    st.success(
        f"{revision_subject} marked complete for {revision_round}"
    )

# =========================================================
# MOCK TEST TRACKER
# =========================================================

st.subheader("📝 Mock Test Tracker")

mock_col1, mock_col2 = st.columns(2)

mock_subject = mock_col1.selectbox(
    "Choose Subject",
    list(subjects.keys()),
    key="mock_subject"
)

mock_score = mock_col2.slider(
    "Mock Test Score",
    0,
    100,
    50
)

if st.button("Save Mock Result"):

    st.success(
        f"Saved score for {mock_subject}: {mock_score}"
    )

# =========================================================
# DAILY DISCIPLINE TRACKER
# =========================================================

st.subheader("✅ Daily Discipline Tracker")

d1 = st.checkbox(
    "1 Hour Revision of Old Topics"
)

d2 = st.checkbox(
    "1 Hour Question Practice"
)

d3 = st.checkbox(
    "15–20 Minutes Formula Revision"
)

d4 = st.checkbox(
    "Completed Daily Lecture Target"
)

d5 = st.checkbox(
    "No Backlog Created"
)

discipline_score = sum([
    d1,
    d2,
    d3,
    d4,
    d5
])

st.metric(
    "🔥 Discipline Score",
    f"{discipline_score}/5"
)

# =========================================================
# SUBJECT PRIORITY
# =========================================================

st.subheader("📌 Subject Priority Strategy")

priority_df = pd.DataFrame({
    "Priority": [
        "1",
        "2",
        "3",
        "4"
    ],
    "Subject": [
        "IDT",
        "DT",
        "FR + AFM",
        "Audit"
    ],
    "Reason": [
        "Quick completion and confidence boost",
        "Largest syllabus and revision heavy",
        "Practical subjects need consistency",
        "Theory subject needs repeated revision"
    ]
})

st.table(priority_df)

# =========================================================
# MOTIVATION
# =========================================================

st.subheader("💡 Motivation Reminder")

st.info("""
Consistency beats motivation.

Lecture completion alone is not enough.
Revision + Practice + Mock Tests will decide your rank and results.
""")

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "CA Final Nov 2026 Dashboard • Built with Streamlit"
)
