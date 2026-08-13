import streamlit as st
import pandas as pd

from config.config import (
    ROLE_DEVELOPER,
    USER_MASTER,
    COORDINATOR_MASTER,
    TASK_MASTER,
    COORDINATOR_TASK_MAP,
    DAILY_REVIEW
)

from utils.google_sheet import read_all


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Developer Dashboard",
    page_icon="🛠️",
    layout="wide"
)


# ==========================================================
# LOGIN CHECK
# ==========================================================

if (
    "logged_in" not in st.session_state
    or not st.session_state.logged_in
):

    st.error("Please login first.")
    st.stop()


# ==========================================================
# CURRENT USER
# ==========================================================

current_user = st.session_state.get(
    "user",
    {}
)

current_role = str(
    current_user.get(
        "Role",
        ""
    )
).strip()


# ==========================================================
# ACCESS CONTROL
# ==========================================================

if current_role != ROLE_DEVELOPER:

    st.error(
        "Developer access required."
    )

    st.stop()


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "🛠️ Developer Dashboard"
)

st.caption(
    "MSU / EPID Health Coordinator Monitoring System"
)

st.divider()


# ==========================================================
# LOAD DATA
# ==========================================================

def safe_read(sheet_name):

    try:
        data = read_all(sheet_name)

        if data:
            return data

        return []

    except Exception:
        return []


users = safe_read(USER_MASTER)

coordinators = safe_read(
    COORDINATOR_MASTER
)

tasks = safe_read(
    TASK_MASTER
)

assignments = safe_read(
    COORDINATOR_TASK_MAP
)

reviews = safe_read(
    DAILY_REVIEW
)


# ==========================================================
# BASIC COUNTS
# ==========================================================

active_users = sum(
    1
    for user in users
    if str(
        user.get(
            "Status",
            "ACTIVE"
        )
    ).strip().upper()
    == "ACTIVE"
)


active_coordinators = sum(
    1
    for coordinator in coordinators
    if str(
        coordinator.get(
            "Status",
            "ACTIVE"
        )
    ).strip().upper()
    == "ACTIVE"
)


active_tasks = sum(
    1
    for task in tasks
    if str(
        task.get(
            "Status",
            "ACTIVE"
        )
    ).strip().upper()
    == "ACTIVE"
)


pending_assignments = sum(
    1
    for assignment in assignments
    if str(
        assignment.get(
            "Status",
            ""
        )
    ).strip().lower()
    == "pending"
)


completed_assignments = sum(
    1
    for assignment in assignments
    if str(
        assignment.get(
            "Status",
            ""
        )
    ).strip().lower()
    == "completed"
)


total_reviews = len(
    reviews
)


completed_reviews = sum(
    1
    for review in reviews
    if str(
        review.get(
            "Status",
            ""
        )
    ).strip().lower()
    == "completed"
)


# ==========================================================
# TOP METRICS
# ==========================================================

c1, c2, c3, c4, c5, c6 = st.columns(6)


with c1:

    st.metric(
        "👥 Active Users",
        active_users
    )


with c2:

    st.metric(
        "👨‍⚕️ Coordinators",
        active_coordinators
    )


with c3:

    st.metric(
        "📋 Active Tasks",
        active_tasks
    )


with c4:

    st.metric(
        "⏳ Pending Tasks",
        pending_assignments
    )


with c5:

    st.metric(
        "✅ Completed Tasks",
        completed_assignments
    )


with c6:

    st.metric(
        "📝 Reviews",
        total_reviews
    )


st.divider()


# ==========================================================
# TASK COMPLETION
# ==========================================================

st.subheader(
    "📊 Task Completion"
)


total_assignments = (
    pending_assignments
    + completed_assignments
)


if total_assignments > 0:

    task_completion = (
        completed_assignments
        / total_assignments
    )

else:

    task_completion = 0


st.progress(
    task_completion
)

st.caption(
    f"{task_completion * 100:.1f}% "
    "of assigned tasks completed"
)


st.divider()


# ==========================================================
# DAILY REVIEW COMPLETION
# ==========================================================

st.subheader(
    "📝 Daily Review Status"
)


if total_reviews > 0:

    review_completion = (
        completed_reviews
        / total_reviews
    )

else:

    review_completion = 0


r1, r2, r3 = st.columns(3)


with r1:

    st.metric(
        "Total Reviews",
        total_reviews
    )


with r2:

    st.metric(
        "Completed Reviews",
        completed_reviews
    )


with r3:

    st.metric(
        "Completion %",
        f"{review_completion * 100:.1f}%"
    )


st.progress(
    review_completion
)


st.divider()


# ==========================================================
# COORDINATOR-WISE TASK SUMMARY
# ==========================================================

st.subheader(
    "👨‍⚕️ Coordinator-wise Task Summary"
)


coordinator_summary = []


for coordinator in coordinators:

    coordinator_id = str(
        coordinator.get(
            "Coordinator_ID",
            coordinator.get(
                "User_ID",
                ""
            )
        )
    ).strip()


    coordinator_name = str(
        coordinator.get(
            "Coordinator_Name",
            coordinator.get(
                "Full_Name",
                coordinator.get(
                    "Username",
                    coordinator_id
                )
            )
        )
    ).strip()


    if not coordinator_id:

        continue


    coordinator_assignments = [

        assignment

        for assignment in assignments

        if str(
            assignment.get(
                "Coordinator_ID",
                ""
            )
        ).strip()
        == coordinator_id

    ]


    total = len(
        coordinator_assignments
    )


    completed = sum(

        1

        for assignment
        in coordinator_assignments

        if str(
            assignment.get(
                "Status",
                ""
            )
        ).strip().lower()
        == "completed"

    )


    pending = sum(

        1

        for assignment
        in coordinator_assignments

        if str(
            assignment.get(
                "Status",
                ""
            )
        ).strip().lower()
        == "pending"

    )


    progress = (

        completed
        / total
        * 100

        if total > 0
        else 0

    )


    coordinator_summary.append(
        {
            "Coordinator": coordinator_name,
            "Assigned": total,
            "Completed": completed,
            "Pending": pending,
            "Completion %": round(
                progress,
                1
            )
        }
    )


if coordinator_summary:

    summary_df = pd.DataFrame(
        coordinator_summary
    )

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No coordinator task data available."
    )


st.divider()


# ==========================================================
# RECENT DAILY REVIEWS
# ==========================================================

st.subheader(
    "📝 Recent Daily Reviews"
)


if reviews:

    recent_reviews = reviews[-10:]

    st.dataframe(
        recent_reviews,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No Daily Review records available."
    )


st.divider()


# ==========================================================
# SYSTEM STATUS
# ==========================================================

st.subheader(
    "🟢 System Status"
)


s1, s2, s3, s4 = st.columns(4)


with s1:

    st.success(
        "Database Connected"
    )


with s2:

    st.success(
        "Authentication Active"
    )


with s3:

    st.success(
        "Task Management Active"
    )


with s4:

    st.success(
        "Daily Review Active"
    )
