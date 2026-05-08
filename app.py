import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Editable Lecture Tracker",
    page_icon="📚",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("📚 CA Final Editable Lecture Tracker")

st.markdown("""
Update your completed lecture hours daily and track progress automatically.
""")

# =========================================================
# INITIAL DATA
# =========================================================

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

# =========================================================
# EDITABLE TABLE
# =========================================================

st.subheader("✏️ Edit Lecture Progress")

edited_df = st.data_editor(
    st.session_state.subjects,
    use_container_width=True,
    num_rows="fixed"
)

# Save updated data
st.session_state.subjects = edited_df

# =========================================================
# CALCULATIONS
# =========================================================

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

# =========================================================
# DISPLAY UPDATED TABLE
# =========================================================

st.subheader("📋 Updated Progress")

st.dataframe(
    edited_df,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# OVERALL PROGRESS
# =========================================================

total_hours = edited_df["Total Hours"].sum()

completed_hours = edited_df["Completed Hours"].sum()

remaining_hours = edited_df["Remaining Hours"].sum()

overall_completion = round(
    (completed_hours / total_hours) * 100,
    2
)

st.subheader("📈 Overall Progress")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Hours",
    total_hours
)

col2.metric(
    "Completed Hours",
    completed_hours
)

col3.metric(
    "Remaining Hours",
    remaining_hours
)

col4.metric(
    "Overall Completion",
    f"{overall_completion}%"
)

st.progress(overall_completion / 100)

# =========================================================
# SUBJECT PROGRESS BARS
# =========================================================

st.subheader("📊 Subject Wise Progress")

for index, row in edited_df.iterrows():

    st.write(
        f"### {row['Subject']} — {row['Completion %']}%"
    )

    st.progress(
        row["Completion %"] / 100
    )

# =========================================================
# DAILY UPDATE SECTION
# =========================================================

st.subheader("➕ Add Daily Lecture Hours")

subject_selected = st.selectbox(
    "Choose Subject",
    edited_df["Subject"]
)

hours_added = st.number_input(
    "Hours Studied Today",
    min_value=0.0,
    max_value=24.0,
    step=0.5
)

if st.button("Update Progress"):

    row_index = edited_df[
        edited_df["Subject"] == subject_selected
    ].index[0]

    current_hours = edited_df.loc[
        row_index,
        "Completed Hours"
    ]

    total_hours_subject = edited_df.loc[
        row_index,
        "Total Hours"
    ]

    updated_hours = current_hours + hours_added

    if updated_hours > total_hours_subject:

        updated_hours = total_hours_subject

    edited_df.loc[
        row_index,
        "Completed Hours"
    ] = updated_hours

    st.session_state.subjects = edited_df

    st.success(
        f"{hours_added} hours added to {subject_selected}"
    )

# =========================================================
# MOTIVATION
# =========================================================

st.subheader("🔥 Daily Reminder")

st.info("""
Small daily progress creates massive results.

Consistency + Revision + Mock Tests = CA Final Success.
""")

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption("Editable CA Final Lecture Tracker")
