import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="CA Final Tracker",
    page_icon="📚",
    layout="wide"
)

# =====================================
# DATABASE
# =====================================

conn = sqlite3.connect("study_tracker.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS study_logs (
    date TEXT,
    subject TEXT,
    hours REAL,
    topic TEXT
)
""")

conn.commit()

# =====================================
# TITLE
# =====================================

st.title("📚 CA Final Nov 2026 Tracker")

# =====================================
# EXAM COUNTDOWN
# =====================================

exam_date = datetime(2026, 11, 2)
today = datetime.today()

days_left = (exam_date - today).days

st.metric("Days Left For Exams", days_left)

# =====================================
# SUBJECT DATA
# =====================================

if "subjects" not in st.session_state:

    st.session_state.subjects = pd.DataFrame({
        "Subject": [
            "FR",
            "AFM",
            "DT",
            "IDT",
            "Audit"
        ],
        "Total Hours": [
            200,
            200,
            200,
            110,
            110
        ],
        "Completed Hours": [
            0,
            0,
            10,
            65,
            0
        ]
    })

# =====================================
# EDITABLE TRACKER
# =====================================

st.subheader("Lecture Tracker")

edited_df = st.data_editor(
    st.session_state.subjects,
    use_container_width=True
)

# =====================================
# AUTO CALCULATIONS
# =====================================

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

st.session_state.subjects = edited_df

# =====================================
# SHOW TABLE
# =====================================

st.dataframe(
    edited_df,
    use_container_width=True,
    hide_index=True
)

# =====================================
# OVERALL PROGRESS
# =====================================

total_hours = edited_df["Total Hours"].sum()

completed_hours = edited_df["Completed Hours"].sum()

overall_progress = round(
    (completed_hours / total_hours) * 100,
    2
)

st.metric(
    "Overall Completion",
    f"{overall_progress}%"
)

st.progress(overall_progress / 100)

# =====================================
# DAILY TARGET
# =====================================

remaining_hours = edited_df["Remaining Hours"].sum()

daily_target = round(
    remaining_hours / max(days_left, 1),
    2
)

st.metric(
    "Daily Hours Needed",
    daily_target
)

# =====================================
# DAILY STUDY LOG
# =====================================

st.subheader("Daily Study Log")

with st.form("study_form"):

    study_date = st.date_input("Date")

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

    submit = st.form_submit_button("Save")

    if submit:

        cursor.execute("""
        INSERT INTO study_logs (
            date,
            subject,
            hours,
            topic
        )
        VALUES (?, ?, ?, ?)
        """, (
            str(study_date),
            subject,
            hours,
            topic
        ))

        conn.commit()

        # AUTO UPDATE HOURS

        row_index = edited_df[
            edited_df["Subject"] == subject
        ].index[0]

        current_hours = edited_df.loc[
            row_index,
            "Completed Hours"
        ]

        total_subject_hours = edited_df.loc[
            row_index,
            "Total Hours"
        ]

        updated_hours = current_hours + hours

        if updated_hours > total_subject_hours:

            updated_hours = total_subject_hours

        edited_df.loc[
            row_index,
            "Completed Hours"
        ] = updated_hours

        st.session_state.subjects = edited_df

        st.success("Study log saved")

# =====================================
# SHOW STUDY LOGS
# =====================================

st.subheader("Study History")

logs_df = pd.read_sql_query(
    "SELECT * FROM study_logs",
    conn
)

st.dataframe(
    logs_df,
    use_container_width=True,
    hide_index=True
)

# =====================================
# REVISION TRACKER
# =====================================

st.subheader("Revision Tracker")

if "revision" not in st.session_state:

    st.session_state.revision = pd.DataFrame({
        "Subject": [
            "FR",
            "AFM",
            "DT",
            "IDT",
            "Audit"
        ],
        "1st Revision": [
            False,
            False,
            False,
            False,
            False
        ],
        "2nd Revision": [
            False,
            False,
            False,
            False,
            False
        ],
        "Final Revision": [
            False,
            False,
            False,
            False,
            False
        ]
    })

revision_df = st.data_editor(
    st.session_state.revision,
    use_container_width=True
)

st.session_state.revision = revision_df

# =====================================
# DAILY TASKS
# =====================================

st.subheader("Today's Focus")

priority_df = edited_df.sort_values(
    by="Remaining Hours",
    ascending=False
).head(3)

for index, row in priority_df.iterrows():

    st.write(
        f"• {row['Subject']} → {row['Remaining Hours']} hrs remaining"
    )

# =====================================
# FOOTER
# =====================================

st.markdown("---")

st.caption("CA Final Smart Tracker")
