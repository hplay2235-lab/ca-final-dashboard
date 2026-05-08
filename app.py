import streamlit as st 
import pandas as pd 
import plotly.express as px 
import sqlite3 
from datetime import datetime, timedelta

=========================================================

PAGE CONFIG

=========================================================

st.set_page_config( page_title="Advanced CA Final Dashboard", page_icon="📚", layout="wide", initial_sidebar_state="expanded" )

=========================================================

DARK MODE CSS

=========================================================

st.markdown("""

<style>

body {
    background-color: #0f172a;
}

.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 1rem;
}

.metric-card {
    background-color: #111827;
    padding: 18px;
    border-radius: 15px;
}

</style>""", unsafe_allow_html=True)

=========================================================

DATABASE

=========================================================

conn = sqlite3.connect("ca_dashboard.db") cursor = conn.cursor()

cursor.execute(''' CREATE TABLE IF NOT EXISTS study_logs ( id INTEGER PRIMARY KEY AUTOINCREMENT, study_date TEXT, subject TEXT, chapter TEXT, hours REAL, topic TEXT ) ''')

conn.commit()

=========================================================

TITLE

=========================================================

st.title("📚 Advanced CA Final Nov 2026 Dashboard")

st.markdown(""" Complete preparation operating system for:

Lecture Tracking

Chapter Tracking

Revision Scheduling

Daily Task Generation

AI Suggestions

Study Analytics """)


=========================================================

EXAM COUNTDOWN

=========================================================

exam_date = datetime(2026, 11, 2) today = datetime.today() remaining_days = (exam_date - today).days

st.subheader("⏳ Exam Countdown")

c1, c2 = st.columns(2)

c1.metric("Days Remaining", remaining_days) c2.metric("Months Remaining", round(remaining_days / 30, 1))

=========================================================

CHAPTER-WISE SUBJECT DATA

=========================================================

chapters = { "FR": { "Consolidation": 40, "Financial Instruments": 35, "Business Combination": 30, "Ind AS": 50, "Miscellaneous": 45 }, "AFM": { "Forex": 35, "Portfolio": 30, "Capital Budgeting": 40, "Risk Management": 45, "Derivatives": 50 }, "DT": { "Capital Gains": 35, "PGBP": 40, "International Tax": 45, "Assessment": 40, "Deductions": 40 }, "IDT": { "GST Basics": 20, "Supply": 25, "ITC": 20, "Returns": 20, "Customs": 25 }, "Audit": { "Professional Ethics": 20, "Company Audit": 30, "Bank Audit": 20, "Peer Review": 15, "Miscellaneous": 25 } }

=========================================================

SESSION STATE

=========================================================

if "progress_df" not in st.session_state:

rows = []

for subject, chapter_data in chapters.items():

    for chapter, hours in chapter_data.items():

        rows.append({
            "Subject": subject,
            "Chapter": chapter,
            "Total Hours": hours,
            "Completed Hours": 0
        })

st.session_state.progress_df = pd.DataFrame(rows)

=========================================================

EDITABLE TRACKER

=========================================================

st.subheader("✏️ Chapter Wise Lecture Tracker")

edited_df = st.data_editor( st.session_state.progress_df, use_container_width=True, num_rows="fixed" )

edited_df["Remaining Hours"] = ( edited_df["Total Hours"] - edited_df["Completed Hours"] )

edited_df["Completion %"] = round( ( edited_df["Completed Hours"] / edited_df["Total Hours"] ) * 100, 2 )

st.session_state.progress_df = edited_df

=========================================================

OVERALL METRICS

=========================================================

total_hours = edited_df["Total Hours"].sum() completed_hours = edited_df["Completed Hours"].sum() remaining_hours = edited_df["Remaining Hours"].sum()

completion_percentage = round( (completed_hours / total_hours) * 100, 2 )

st.subheader("📈 Overall Progress")

m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Hours", total_hours) m2.metric("Completed", completed_hours) m3.metric("Remaining", remaining_hours) m4.metric("Completion %", f"{completion_percentage}%")

st.progress(completion_percentage / 100)

=========================================================

FORECAST SYSTEM

=========================================================

st.subheader("📅 Completion Forecast")

if completed_hours > 0:

avg_daily_hours = completed_hours / max((datetime.today() - datetime(2026, 5, 1)).days, 1)

if avg_daily_hours > 0:

    estimated_days_needed = remaining_hours / avg_daily_hours

    estimated_completion = today + timedelta(days=estimated_days_needed)

    st.success(
        f"At current speed, lectures may complete by {estimated_completion.strftime('%d %B %Y')}"
    )

=========================================================

CHARTS

=========================================================

st.subheader("📊 Subject Completion Analytics")

subject_summary = edited_df.groupby("Subject")[ ["Total Hours", "Completed Hours"] ].sum().reset_index()

subject_summary["Completion %"] = round( ( subject_summary["Completed Hours"] / subject_summary["Total Hours"] ) * 100, 2 )

fig = px.bar( subject_summary, x="Subject", y="Completion %", text="Completion %", title="Subject Wise Completion" )

fig.update_traces(textposition="outside") fig.update_layout(yaxis_range=[0, 100])

st.plotly_chart(fig, use_container_width=True)

=========================================================

REVISION SCHEDULER

=========================================================

st.subheader("🔁 Smart Revision Scheduler")

revision_days = { "1st Revision": 3, "2nd Revision": 7, "Final Revision": 15 }

for revision_name, gap in revision_days.items():

revision_date = today + timedelta(days=gap)

st.info(
    f"{revision_name} Recommended On: {revision_date.strftime('%d %B %Y')}"
)

=========================================================

DAILY TASK GENERATOR

=========================================================

st.subheader("🎯 AI Daily Task Generator")

remaining_df = edited_df.sort_values( by="Remaining Hours", ascending=False )

priority_subjects = remaining_df.head(3)

for index, row in priority_subjects.iterrows():

suggested_hours = round(row["Remaining Hours"] / max(remaining_days, 1), 1)

st.write(
    f"✅ Study {row['Subject']} - {row['Chapter']} for {suggested_hours} hrs today"
)

=========================================================

DAILY STUDY LOGS

=========================================================

st.subheader("📝 Daily Study Logs")

with st.form("study_log_form"):

study_date = st.date_input("Study Date")

subject = st.selectbox(
    "Subject",
    edited_df["Subject"].unique()
)

chapter_options = edited_df[
    edited_df["Subject"] == subject
]["Chapter"].tolist()

chapter = st.selectbox(
    "Chapter",
    chapter_options
)

hours = st.number_input(
    "Hours Studied",
    min_value=0.0,
    max_value=24.0,
    step=0.5
)

topic = st.text_input("Topic Covered")

submit = st.form_submit_button("Add Study Log")

if submit:

    cursor.execute('''
    INSERT INTO study_logs (
        study_date,
        subject,
        chapter,
        hours,
        topic
    ) VALUES (?, ?, ?, ?, ?)
    ''', (
        str(study_date),
        subject,
        chapter,
        hours,
        topic
    ))

    conn.commit()

    row_index = edited_df[
        (
            edited_df["Subject"] == subject
        )
        &
        (
            edited_df["Chapter"] == chapter
        )
    ].index[0]

    current_hours = edited_df.loc[
        row_index,
        "Completed Hours"
    ]

    total_hours_chapter = edited_df.loc[
        row_index,
        "Total Hours"
    ]

    updated_hours = current_hours + hours

    if updated_hours > total_hours_chapter:
        updated_hours = total_hours_chapter

    edited_df.loc[
        row_index,
        "Completed Hours"
    ] = updated_hours

    st.session_state.progress_df = edited_df

    st.success("Study log added successfully.")

=========================================================

DISPLAY LOGS

=========================================================

logs_df = pd.read_sql_query( "SELECT * FROM study_logs ORDER BY study_date DESC", conn )

st.subheader("📚 Study Log History")

st.dataframe( logs_df, use_container_width=True, hide_index=True )

=========================================================

AI SUGGESTIONS

=========================================================

st.subheader("🤖 AI Study Suggestions")

weak_chapters = edited_df.sort_values( by="Completion %" ).head(3)

for index, row in weak_chapters.iterrows():

st.warning(
    f"Focus more on {row['Subject']} - {row['Chapter']}. Completion is only {row['Completion %']}%"
)

if completion_percentage < 30:

st.error(
    "Lecture completion pace is slow. Increase study hours immediately."
)

elif completion_percentage < 60:

st.info(
    "Progress is decent but revision phase should begin soon."
)

else:

st.success(
    "Excellent pace. Continue revision and mock test practice consistently."
)

=========================================================

DAILY TARGETS

=========================================================

st.subheader("🎯 Smart Daily Targets")

if remaining_days > 0:

daily_target = round(
    remaining_hours / remaining_days,
    2
)

weekly_target = round(
    remaining_hours / (remaining_days / 7),
    2
)

d1, d2 = st.columns(2)

d1.metric(
    "Daily Hours Needed",
    daily_target
)

d2.metric(
    "Weekly Hours Needed",
    weekly_target
)

=========================================================

FOOTER

=========================================================

st.markdown("---")

st.caption("Advanced CA Final Dashboard • Production Ready")
