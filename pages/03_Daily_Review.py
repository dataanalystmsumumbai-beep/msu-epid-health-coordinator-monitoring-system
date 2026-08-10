import streamlit as st
from datetime import date, datetime

from config.config import DAILY_REVIEW
from utils.google_sheet import read_all, insert_row


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Daily Review",
    page_icon="📝",
    layout="wide"
)


# ============================================================
# SESSION CHECK
# ============================================================

if not st.session_state.get("logged_in", False):
    st.error("Please login first.")
    st.stop()


# ============================================================
# GET CURRENT USER
# IMPORTANT:
# session.py stores these as separate session_state values.
# Do NOT use st.session_state["user"] here.
# ============================================================

current_username = str(
    st.session_state.get("username", "")
).strip()

current_role = str(
    st.session_state.get("role", "")
).strip()

current_name = str(
    st.session_state.get(
        "full_name",
        current_username
    )
).strip()

current_user_id = str(
    st.session_state.get("user_id", "")
).strip()


# ============================================================
# NORMALIZE ROLE
# ============================================================

role = current_role.lower().strip()


# ============================================================
# HEADER
# ============================================================

st.title("📝 Daily Review")

st.caption(
    f"User: {current_name}  |  Role: {current_role}"
)

st.divider()


# ============================================================
# VALID ROLE CHECK
# ============================================================

allowed_roles = [
    "developer",
    "admin",
    "coordinator"
]

if role not in allowed_roles:

    st.error(
        "⛔ You do not have permission to access Daily Review."
    )

    st.stop()


# ============================================================
# LOAD DAILY REVIEW DATA
# ============================================================

try:

    review_records = read_all(DAILY_REVIEW)

except Exception as e:

    review_records = []

    st.warning(
        "Daily Review data could not be loaded from Google Sheets."
    )


# ============================================================
# COORDINATOR - SUBMIT DAILY REVIEW
# ============================================================

if role == "coordinator":

    st.subheader("📋 Submit Daily Review")

    with st.form(
        "daily_review_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(2)

        with col1:

            review_date = st.date_input(
                "Review Date",
                value=date.today()
            )

        with col2:

            task_name = st.text_input(
                "Task / Activity",
                placeholder="Enter task or activity name"
            )

        status = st.selectbox(
            "Status",
            [
                "COMPLETED",
                "PENDING",
                "IN PROGRESS"
            ]
        )

        remarks = st.text_area(
            "Remarks",
            placeholder="Enter remarks / observations",
            height=120
        )

        submitted = st.form_submit_button(
            "✅ Submit Daily Review",
            use_container_width=True
        )

    if submitted:

        if not task_name.strip():

            st.error(
                "Please enter the Task / Activity."
            )

        else:

            try:

                review_id = (
                    "REV-"
                    + datetime.now().strftime(
                        "%Y%m%d%H%M%S"
                    )
                )

                current_time = datetime.now().strftime(
                    "%d-%m-%Y %H:%M"
                )

                new_row = [

                    review_id,

                    review_date.strftime(
                        "%d-%m-%Y"
                    ),

                    current_user_id,

                    task_name.strip(),

                    status,

                    remarks.strip(),

                    current_time,

                    current_time

                ]

                insert_row(
                    DAILY_REVIEW,
                    new_row
                )

                st.success(
                    "✅ Daily Review submitted successfully."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Unable to save Daily Review: {e}"
                )


# ============================================================
# ADMIN / DEVELOPER - MONITORING
# ============================================================

if role in [
    "admin",
    "developer"
]:

    st.subheader(
        "📊 Daily Review Monitoring"
    )

    if not review_records:

        st.info(
            "No Daily Review records available."
        )

    else:

        # ----------------------------------------------------
        # BUILD DISPLAY DATA
        # ----------------------------------------------------

        display_records = []

        for record in review_records:

            display_records.append(
                {
                    "Review ID": record.get(
                        "Review_ID",
                        ""
                    ),

                    "Date": record.get(
                        "Review_Date",
                        record.get(
                            "Date",
                            ""
                        )
                    ),

                    "Coordinator": record.get(
                        "Coordinator_ID",
                        record.get(
                            "Coordinator_Name",
                            record.get(
                                "Username",
                                ""
                            )
                        )
                    ),

                    "Task": record.get(
                        "Task_ID",
                        record.get(
                            "Task",
                            record.get(
                                "Task_Name",
                                record.get(
                                    "Activity",
                                    ""
                                )
                            )
                        )
                    ),

                    "Status": record.get(
                        "Status",
                        ""
                    ),

                    "Remarks": record.get(
                        "Remarks",
                        ""
                    ),

                    "Submitted On": record.get(
                        "Created_On",
                        record.get(
                            "Submitted_On",
                            ""
                        )
                    ),

                    "Modified On": record.get(
                        "Modified_On",
                        ""
                    )
                }
            )


        # ----------------------------------------------------
        # METRICS
        # ----------------------------------------------------

        active_records = [
            row
            for row in display_records
            if str(
                row["Status"]
            ).strip().upper() != "DELETED"
        ]

        total_count = len(active_records)

        completed_count = sum(
            1
            for row in active_records
            if str(
                row["Status"]
            ).strip().upper()
            == "COMPLETED"
        )

        pending_count = sum(
            1
            for row in active_records
            if str(
                row["Status"]
            ).strip().upper()
            == "PENDING"
        )

        in_progress_count = sum(
            1
            for row in active_records
            if str(
                row["Status"]
            ).strip().upper()
            == "IN PROGRESS"
        )


        # ----------------------------------------------------
        # METRIC CARDS
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Total Reviews",
                total_count
            )

        with col2:

            st.metric(
                "Completed",
                completed_count
            )

        with col3:

            st.metric(
                "Pending",
                pending_count
            )

        with col4:

            st.metric(
                "In Progress",
                in_progress_count
            )


        st.divider()


        # ----------------------------------------------------
        # COMPLETION RATE
        # ----------------------------------------------------

        if total_count > 0:

            completion_rate = round(
                (
                    completed_count
                    / total_count
                ) * 100,
                2
            )

        else:

            completion_rate = 0


        st.subheader(
            "📈 Overall Completion"
        )

        st.progress(
            completion_rate / 100
        )

        st.caption(
            f"Completion Rate: {completion_rate}%"
        )


        st.divider()


        # ----------------------------------------------------
        # REVIEW TABLE
        # ----------------------------------------------------

        st.subheader(
            "📋 Submitted Reviews"
        )

        st.dataframe(
            active_records,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# END
# ============================================================
