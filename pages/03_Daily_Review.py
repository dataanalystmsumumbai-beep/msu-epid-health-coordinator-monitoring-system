import streamlit as st
from datetime import date, datetime, timedelta

from core.navigation import require_login
from core.session import current_user

from services.review_service import ReviewService
from services.task_assignment_service import TaskAssignmentService


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Daily Review",
    page_icon="📝",
    layout="wide"
)


# ==========================================================
# LOGIN
# ==========================================================

require_login(
    ["Admin", "Coordinator", "Developer"]
)


user = current_user()

current_role = str(
    user.get(
        "role",
        ""
    )
).strip()

current_user_id = str(
    user.get(
        "user_id",
        ""
    )
).strip()


# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("📝 Daily Review")

st.caption(
    "Daily task submission and monitoring"
)


# ==========================================================
# HELPERS
# ==========================================================

def normalize(value):

    return str(
        value
        if value is not None
        else ""
    ).strip()


def get_task_name(task_id):

    return normalize(
        task_id
    )


def parse_date(value):

    try:

        return datetime.strptime(
            normalize(value),
            "%d-%m-%Y"
        ).date()

    except Exception:

        return None


# ==========================================================
# COORDINATOR VIEW
# ==========================================================

if current_role == "Coordinator":

    st.subheader(
        "📋 My Assigned Tasks"
    )

    assignments = (
        TaskAssignmentService
        .get_coordinator_tasks(
            current_user_id
        )
    )


    if not assignments:

        st.info(
            "No active tasks are assigned to you."
        )

        st.stop()


    # ------------------------------------------------------
    # ACTIVE ASSIGNMENTS
    # ------------------------------------------------------

    active_assignments = []


    for assignment in assignments:

        status = normalize(
            assignment.get(
                "Status",
                ""
            )
        ).lower()


        if status not in [
            "removed",
            "inactive",
            "deleted"
        ]:

            active_assignments.append(
                assignment
            )


    if not active_assignments:

        st.info(
            "No active tasks are assigned to you."
        )

        st.stop()


    # ------------------------------------------------------
    # TASK SELECTOR
    # ------------------------------------------------------

    task_options = []


    for assignment in active_assignments:

        task_id = normalize(
            assignment.get(
                "Task_ID",
                ""
            )
        )

        if task_id:

            task_options.append(
                task_id
            )


    task_options = list(
        dict.fromkeys(
            task_options
        )
    )


    selected_task = st.selectbox(
        "Select Task",
        task_options,
        key="daily_review_task"
    )


    # ------------------------------------------------------
    # REVIEW DATE
    # ------------------------------------------------------

    selected_date = st.date_input(
        "Review Date",
        value=date.today(),
        key="daily_review_date"
    )


    review_date = (
        selected_date
        .strftime(
            "%d-%m-%Y"
        )
    )


    # ------------------------------------------------------
    # EXISTING SUBMISSION
    # ------------------------------------------------------

    existing_submission = (
        ReviewService
        .get_submission(
            current_user_id,
            selected_task,
            review_date
        )
    )


    if existing_submission:

        st.success(
            f"✅ Already submitted for {review_date}"
        )


        st.info(
            "This task has already been submitted for "
            "the selected date."
        )


        st.write(
            "**Status:** "
            + normalize(
                existing_submission.get(
                    "Status",
                    ""
                )
            )
        )


        remarks = normalize(
            existing_submission.get(
                "Remarks",
                ""
            )
        )


        if remarks:

            st.write(
                "**Remarks:** "
                + remarks
            )


    else:

        # --------------------------------------------------
        # NEW DAILY SUBMISSION
        # --------------------------------------------------

        st.subheader(
            "📤 Submit Daily Review"
        )


        status = st.selectbox(
            "Task Status",
            [
                "Completed",
                "Pending",
                "In Progress"
            ],
            key="daily_submission_status"
        )


        remarks = st.text_area(
            "Remarks",
            placeholder=(
                "Enter remarks or work details..."
            ),
            key="daily_submission_remarks"
        )


        if st.button(
            "📤 Submit Daily Review",
            type="primary",
            use_container_width=True,
            key="submit_daily_review"
        ):

            success, message = (
                ReviewService
                .create_review(
                    review_date=review_date,
                    coordinator_id=current_user_id,
                    task_id=selected_task,
                    status=status,
                    remarks=remarks
                )
            )


            if success:

                st.success(
                    message
                )

                st.rerun()

            else:

                st.error(
                    message
                )


    # ======================================================
    # SUBMISSION HISTORY
    # ======================================================

    st.divider()

    st.subheader(
        "📚 My Submission History"
    )


    history = (
        ReviewService
        .get_reviews_by_coordinator(
            current_user_id
        )
    )


    task_history = [

        row

        for row in history

        if normalize(
            row.get(
                "Task_ID",
                ""
            )
        )
        ==
        selected_task

    ]


    if task_history:

        display_rows = []


        for row in task_history:

            display_rows.append({

                "Date":
                    normalize(
                        row.get(
                            "Date",
                            ""
                        )
                    ),

                "Task":
                    normalize(
                        row.get(
                            "Task_ID",
                            ""
                        )
                    ),

                "Status":
                    normalize(
                        row.get(
                            "Status",
                            ""
                        )
                    ),

                "Remarks":
                    normalize(
                        row.get(
                            "Remarks",
                            ""
                        )
                    ),

                "Submitted At":
                    normalize(
                        row.get(
                            "Submitted_At",
                            ""
                        )
                    )

            })


        st.dataframe(
            display_rows,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No submission history found for this task."
        )


# ==========================================================
# ADMIN / DEVELOPER VIEW
# ==========================================================

else:

    st.subheader(
        "📊 Review Monitoring"
    )


    # ------------------------------------------------------
    # DATE RANGE
    # ------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        from_date = st.date_input(
            "From Date",
            value=date.today(),
            key="review_from_date"
        )


    with col2:

        to_date = st.date_input(
            "To Date",
            value=date.today(),
            key="review_to_date"
        )


    if from_date > to_date:

        st.error(
            "From Date cannot be greater than To Date."
        )

        st.stop()


    # ------------------------------------------------------
    # GET REVIEWS
    # ------------------------------------------------------

    reviews = (
        ReviewService
        .get_reviews_by_date_range(
            from_date.strftime(
                "%d-%m-%Y"
            ),
            to_date.strftime(
                "%d-%m-%Y"
            )
        )
    )


    # ------------------------------------------------------
    # FILTERS
    # ------------------------------------------------------

    coordinators = [

        normalize(
            row.get(
                "Coordinator_ID",
                ""
            )
        )

        for row in reviews

        if normalize(
            row.get(
                "Coordinator_ID",
                ""
            )
        )

    ]


    tasks = [

        normalize(
            row.get(
                "Task_ID",
                ""
            )
        )

        for row in reviews

        if normalize(
            row.get(
                "Task_ID",
                ""
            )
        )

    ]


    coordinators = sorted(
        list(
            dict.fromkeys(
                coordinators
            )
        )
    )


    tasks = sorted(
        list(
            dict.fromkeys(
                tasks
            )
        )
    )


    filter_col1, filter_col2 = st.columns(2)


    with filter_col1:

        selected_coordinator = st.selectbox(
            "Coordinator",
            ["All"] + coordinators,
            key="review_coordinator_filter"
        )


    with filter_col2:

        selected_task_filter = st.selectbox(
            "Task",
            ["All"] + tasks,
            key="review_task_filter"
        )


    filtered_reviews = reviews


    if selected_coordinator != "All":

        filtered_reviews = [

            row

            for row in filtered_reviews

            if normalize(
                row.get(
                    "Coordinator_ID",
                    ""
                )
            )
            ==
            selected_coordinator

        ]


    if selected_task_filter != "All":

        filtered_reviews = [

            row

            for row in filtered_reviews

            if normalize(
                row.get(
                    "Task_ID",
                    ""
                )
            )
            ==
            selected_task_filter

        ]


    # ======================================================
    # SUMMARY
    # ======================================================

    st.divider()

    st.subheader(
        "📈 Review Summary"
    )


    total = len(
        filtered_reviews
    )


    completed = sum(

        1

        for row in filtered_reviews

        if normalize(
            row.get(
                "Status",
                ""
            )
        ).upper()
        == "COMPLETED"

    )


    pending = sum(

        1

        for row in filtered_reviews

        if normalize(
            row.get(
                "Status",
                ""
            )
        ).upper()
        == "PENDING"

    )


    in_progress = sum(

        1

        for row in filtered_reviews

        if normalize(
            row.get(
                "Status",
                ""
            )
        ).upper()

        in [
            "IN PROGRESS",
            "IN_PROGRESS"
        ]

    )


    completion_percentage = (

        round(
            (
                completed
                /
                total
            )
            * 100,
            2
        )

        if total

        else 0

    )


    metric1, metric2, metric3, metric4, metric5 = st.columns(5)


    metric1.metric(
        "Submissions",
        total
    )


    metric2.metric(
        "Completed",
        completed
    )


    metric3.metric(
        "Pending",
        pending
    )


    metric4.metric(
        "In Progress",
        in_progress
    )


    metric5.metric(
        "Completion",
        f"{completion_percentage}%"
    )


    # ======================================================
    # REVIEW TABLE
    # ======================================================

    st.divider()

    st.subheader(
        "📋 Submission Details"
    )


    if filtered_reviews:

        display_rows = []


        for row in filtered_reviews:

            display_rows.append({

                "Date":
                    normalize(
                        row.get(
                            "Date",
                            ""
                        )
                    ),

                "Coordinator":
                    normalize(
                        row.get(
                            "Coordinator_ID",
                            ""
                        )
                    ),

                "Task":
                    normalize(
                        row.get(
                            "Task_ID",
                            ""
                        )
                    ),

                "Status":
                    normalize(
                        row.get(
                            "Status",
                            ""
                        )
                    ),

                "Remarks":
                    normalize(
                        row.get(
                            "Remarks",
                            ""
                        )
                    ),

                "Submitted At":
                    normalize(
                        row.get(
                            "Submitted_At",
                            ""
                        )
                    )

            })


        st.dataframe(
            display_rows,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No submissions found for the selected filters."
        )

