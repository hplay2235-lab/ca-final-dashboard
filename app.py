import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="CA Final Nov 2026 Tracker",
    page_icon="📚",
    layout="wide"
)

# =========================================
# TITLE
# =========================================

st.title("📚 CA Final Nov 2026 Preparation Dashboard")
st.markdown("Track your lectures, revisions, mock tests, and overall preparation progress.")

# =========================================
# EXAM COUNTDOWN
# =========================================

exam_date = datetime(2026, 11, 2)
today = datetime.today()

remaining_days = (exam_date - today).days

st.metric("⏳ Days Remaining for CA Final", remaining_days)

# =========================================
# SUBJECT DATA
# =========================================

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

# =========================================
# CREATE DATAFRAME
# =========================================

data = []

for subject, values in subjects.items():

    total = values["total"]
    completed = values["completed"]
    remaining = total - completed

    completion_percent = round((completed / total) * 100, 2)

    data.append({
        "Subject": subject,
        "Total Hours": total,
        "Completed Hours": completed,
        "Remaining Hours": remaining,
        "Completion %": completion_percent
    })

df = pd.DataFrame(data)

# =========================================
# OVERALL PROGRESS
# =========================================

total_hours = df["Total Hours"].sum()
completed_hours = df["Completed Hours"].sum()
remaining_hours = df["Remaining Hours"].sum()

overall_completion = round(
    (completed_hours / total_hours) * 100,
    2
)

st.subheader("📈 Overall Progress")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Hours", total_hours)
col2.metric("Completed", completed_hours)
col3.metric("Remaining", remaining_hours)
col4.metric("Overall Completion", f"{overall_completion}%")

st.progress(overall_completion / 100)

# =========================================
# SUBJECT TABLE
# =========================================

st.subheader("📋 Subject-Wise Progress")

st.dataframe(df, use_container_width=True)

# =========================================
# BAR CHART
# =========================================

st.subheader("📊 Subject Completion Chart")

fig = px.bar(
    df,
    x="Subject",
    y="Completion %",
    text="Completion %",
    title="Lecture Completion Percentage"
)

fig.update_traces(textposition="outside")

fig.update_layout(
    yaxis_range=[0, 100]
)

st.plotly_chart(fig, use_container_width=True)

# =========================================
# DAILY TARGET CALCULATOR
# =========================================

st.subheader("🎯 Daily Target Calculator")

weeks_remaining = remaining_days // 7

if weeks_remaining > 0:

    daily_target = round(
        remaining_hours / remaining_days,
        2
    )

    weekly_target = round(
        remaining_hours / weeks_remaining,
        2
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Daily Lecture Hours Needed",
        daily_target
    )

    col2.metric(
        "Weekly Lecture Hours Needed",
        weekly_target
    )

# =========================================
# MONTHLY TARGETS
# =========================================

st.subheader("🗓️ Monthly Targets")

monthly_targets = pd.DataFrame({
    "Month": [
        "May 2026",
        "June 2026",
        "July 2026",
        "August 2026",
        "September 2026",
        "October 2026"
    ],
    "Goal": [
        "Finish IDT + Strong DT Start",
        "Heavy DT + FR Progress",
        "Finish DT + Continue FR + Start AFM",
        "Complete All Lectures",
        "1st Full Revision",
        "Mocks + Final Revision"
    ]
})

st.table(monthly_targets)

# =========================================
# DAILY STUDY SCHEDULE
# =========================================

st.subheader("⏰ Ideal Daily Study Schedule")

schedule_df = pd.DataFrame({
    "Time": [
        "6:30 – 8:30 AM",
        "9:00 – 1:00 PM",
        "2:00 – 5:00 PM",
        "6:00 – 8:00 PM",
        "9:00 – 10:00 PM"
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

# =========================================
# REVISION TRACKER
# =========================================

st.subheader("🔁 Revision Tracker")

revision_subject = st.selectbox(
    "Select Subject",
    list(subjects.keys())
)

revision
