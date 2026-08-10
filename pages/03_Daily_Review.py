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


current_user = st.session_state.get("user", {})

if not isinstance(current_user, dict):
    current_user = {}


current_username = str(
    current_user.get("Username", "")
).strip()

current_role = str(
    current_user.get("Role", "")
).strip()

current_name = str(
    current_user.get("Full_Name", current_username)
).strip()


# ============================================================
# HEADER
# ============================================================

st.title("📝 Daily Review")

st.caption(
    f"User: {current_name}  |  Role: {current_role}"
)

st.divider()


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
# COORDINATOR - SUBMIT REVIEW
# ============================================================

if current_role.lower() == "coordinator":

    st.subheader("📋 Submit Daily Review")

    with st.form("daily_review_form", clear_on_submit=False):

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
                "Completed",
                "Pending",
                "In Progress"
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

                new_row = [
                    datetime.now().strftime("%Y%m%d%H%M%S"),
                    review_date.strftime("%d-%m-%Y"),
                    current_username,
                    current_name,
                    task_name.strip(),
                    status,
                    remarks.strip(),
                    datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                ]

                insert_row(
                    DAILY_REVIEW,
                    new_row
                )

                st.success(
                    "Daily Review submitted successfully."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Unable to save Daily Review: {e}"
                )


# ============================================================
# ADMIN / DEVELOPER VIEW
# ============================================================

if current_role.lower() in ["admin", "developer"]:

    st.subheader("📊 Daily Review Monitoring")

    if not review_records:

        st.info(
            "No Daily Review records available."
        )

    else:

        # ----------------------------------------------------
        # Convert records for display
        # ----------------------------------------------------

        display_records = []

        for record in review_records:

            display_records.append(
                {
                    "Date": record.get(
                        "Review_Date",
                        record.get("Date", "")
                    ),

                    "Coordinator": record.get(
                        "Full_Name",
                        record.get(
                            "Coordinator_Name",
                            record.get("Username", "")
                        )
                    ),

                    "Task": record.get(
                        "Task",
                        record.get(
                            "Task_Name",
                            record.get("Activity", "")
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
                        "Submitted_On",
                        record.get(
                            "Created_On",
                            ""
                        )
                    )
                }
            )

        # ----------------------------------------------------
        # Metrics
        # ----------------------------------------------------

        completed_count = sum(
            1
            for row in display_records
            if str(row["Status"]).strip().lower()
            == "completed"
        )

        pending_count = sum(
            1
            for row in display_records
            if str(row["Status"]).strip().lower()
            == "pending"
        )

        in_progress_count = sum(
            1
            for row in display_records
            if str(row["Status"]).strip().lower()
            == "in progress"
        )

        total_count = len(display_records)

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
        # Review Table
        # ----------------------------------------------------

        st.subheader("📋 Submitted Reviews")

        st.dataframe(
            display_records,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# FALLBACK FOR OTHER ROLES
# ============================================================

if current_role.lower() not in [
    "coordinator",
    "admin",
    "developer"
]:

    st.warning(
        "You do not have permission to access Daily Review."
    )
