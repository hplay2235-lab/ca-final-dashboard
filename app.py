import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime, timedelta

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CA Final Dashboard",
    page_icon="📚",
    layout="wide"
)

# =========================================================
# DATABASE CONNECTION
# =========================================================

conn = sqlite3.connect("database/ca_dashboard.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS study_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_date TEXT,
    subject TEXT,
    chapter TEXT,
    hours REAL,
    topic TEXT
)
''')

conn.commit()

# =========================================================
# SUBJECT DATA
# =========================================================

subjects = {
    "FR": 200,
    "AFM": 200,
    "DT": 200,
    "IDT": 110,
    "Audit": 110
}

# =========================================================
# SESSION STATE
# =========================================================

if "progress_df" not in st.session_state:

    st.session_state.progress_df = pd.DataFrame({
        "Subject": list(subjects.keys()),
        "Total Hours": list(subjects.values()),
        "Completed Hours": [0, 0, 10, 65, 0]
    })

# =========================================================
# TITLE
# =========================================================

st.title("📚 CA Final Nov 2026 Dashboard")

st.markdown("Track lectures, revisions, study logs, and progress.")

# =========================================================
# EXAM COUNTDOWN
# =========================================================

exam_date = datetime(2026, 11, 2)
today = datetime.today()

remaining_days = (exam_date - today).days

col1, col2 = st.columns(2)

col1.metric("Days Remaining", remaining_days)
col2.metric("Months Remaining", round(remaining_days / 30, 1))

# =========================================================
# EDITABLE TRACKER
# =========================================================

st.subheader("✏️ Lecture Tracker")

edited_df = st.data_editor(
    st.session_state.progress_df,
    use_container_width=True,
    num_rows="fixed"
)

edited_df["Remaining Hours"] = (
    edited_df["Total Hours"]
    - edited_df["Completed Hours"]
)

edited_df["Completion %"] = round(
    (
        edited_df["Completed Hours"]
        / edited_df["Total Hours"]
    ) * 100,
    2
)

st.session_state.progress_df = edited_df

# =========================================================
# OVERALL METRICS
# =========================================================

st.subheader("📈 Overall Progress")

total_hours = edited_df["Total Hours"].sum()
completed_hours = edited_df["Completed Hours"].sum()
remaining_hours = edited_df["Remaining Hours"].sum()

completion_percentage = round(
    (completed_hours / total_hours) * 100,
    2
)

m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Hours", total_hours)
m2.metric("Completed", completed_hours)
m3.metric("Remaining", remaining_hours)
m4.metric("Completion", f"{completion_percentage}%")

st.progress(completion_percentage / 100)

# =========================================================
# CHART
# =========================================================

st.subheader("📊 Completion Chart")

fig = px.bar(
    edited_df,
    x="Subject",
    y="Completion %",
    text="Completion %"
)

fig.update_traces(textposition="outside")
fig.update_layout(yaxis_range=[0, 100])

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# DAILY STUDY LOGS
# =========================================================

st.subheader("📝 Daily Study Logs")

with st.form("study_log_form"):

    study_date = st.date_input("Study Date")

    subject = st.selectbox(
        "Subject",
        edited_df["Subject"]
    )

    hours = st.number_input(
        "Hours Studied",
        min_value=0.0,
        max_value=24.0,
        step=0.5
    )

    topic = st.text_input("Topic Covered")

    submitted = st.form_submit_button("Add Log")

    if submitted:

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
            "General",
            hours,
            topic
        ))

        conn.commit()

        st.success("Study log added successfully.")

# =========================================================
# SHOW LOGS
# =========================================================

logs_df = pd.read_sql_query(
    "SELECT * FROM study_logs ORDER BY study_date DESC",
    conn
)

st.subheader("📚 Study Log History")

st.dataframe(
    logs_df,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# AI TASK GENERATOR
# =========================================================

st.subheader("🎯 Smart Daily Tasks")

priority_df = edited_df.sort_values(
    by="Remaining Hours",
    ascending=False
).head(3)

for index, row in priority_df.iterrows():

    suggested_hours = round(
        row["Remaining Hours"] / max(remaining_days, 1),
        1
    )

    st.info(
        f"Study {row['Subject']} for {suggested_hours} hrs today"
    )

# =========================================================
# REVISION SCHEDULER
# =========================================================

st.subheader("🔁 Revision Scheduler")

st.write(
    f"1st Revision Suggested: {(today + timedelta(days=3)).strftime('%d %b %Y')}"
)

st.write(
    f"2nd Revision Suggested: {(today + timedelta(days=7)).strftime('%d %b %Y')}"
)

st.write(
    f"Final Revision Suggested: {(today + timedelta(days=15)).strftime('%d %b %Y')}"
)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")
st.caption("CA Final Smart Dashboard")
