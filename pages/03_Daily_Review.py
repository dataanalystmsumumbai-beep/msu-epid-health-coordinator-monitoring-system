import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import calendar

from core.navigation import require_login

from services.task_assignment_service import (
    TaskAssignmentService
)

from services.task_service import (
    TaskService
)

from utils.google_sheet import (
    read_all,
    insert_row,
    update_value
)

from config.config import (
    DAILY_REVIEW,
    COORDINATOR_TASK_MAP,
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Daily Review",
    page_icon="📝",
    layout="wide"
)


# ==========================================================
# ACCESS
# ==========================================================

require_login([
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR
])


# ==========================================================
# SESSION
# ==========================================================

current_username = str(
    st.session_state.get(
        "username",
        ""
    )
).strip()


current_role = str(
    st.session_state.get(
        "role",
        ""
    )
).strip()


current_user_id = str(
    st.session_state.get(
        "user_id",
        current_username
    )
).strip()


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "📝 Daily Review"
)

st.caption(
    f"User: {current_username} | Role: {current_role}"
)

st.divider()


# ==========================================================
# HELPERS
# ==========================================================

def get_value(
    record,
    *keys
):

    if not record:
        return ""

    for key in keys:

        value = record.get(
            key,
            ""
        )

        if (
            value is not None
            and str(value).strip() != ""
        ):

            return value

    return ""


def normalize(
    value
):

    return str(
        value
        if value is not None
        else ""
    ).strip()


def normalize_status(
    value
):

    return normalize(
        value
    ).lower().replace(
        "_",
        " "
    )


def parse_date(
    value
):

    if isinstance(
        value,
        datetime
    ):

        return value.date()


    if isinstance(
        value,
        date
    ):

        return value


    value = normalize(
        value
    )

    if not value:

        return None


    formats = [
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%d-%m-%Y %H:%M",
        "%Y-%m-%d %H:%M:%S"
    ]


    for fmt in formats:

        try:

            return datetime.strptime(
                value,
                fmt
            ).date()

        except Exception:

            continue


    return None


def format_date(
    value
):

    parsed = parse_date(
        value
    )

    if parsed:

        return parsed.strftime(
            "%d-%m-%Y"
        )

    return normalize(
        value
    )


def normalize_frequency(
    value
):

    frequency = normalize(
        value
    ).lower()


    if frequency in [
        "daily",
        "day"
    ]:

        return "Daily"


    if frequency in [
        "weekly",
        "week"
    ]:

        return "Weekly"


    if frequency in [
        "monthly",
        "month"
    ]:

        return "Monthly"


    return "One Time"


# ==========================================================
# LOAD DATA
# ==========================================================

try:

    all_tasks = (
        TaskService
        .get_all_tasks()
    )

except Exception:

    all_tasks = []


try:

    all_assignments = (
        TaskAssignmentService
        .get_all_assignments()
    )

except Exception:

    all_assignments = []


try:

    all_reviews = read_all(
        DAILY_REVIEW
    )

except Exception:

    all_reviews = []


all_tasks = (
    all_tasks
    or []
)


all_assignments = (
    all_assignments
    or []
)


all_reviews = (
    all_reviews
    or []
)


# ==========================================================
# TASK LOOKUP
# ==========================================================

task_lookup = {}


for task in all_tasks:

    task_id = normalize(
        get_value(
            task,
            "Task_ID",
            "Task_Id",
            "ID"
        )
    )


    if task_id:

        task_lookup[
            task_id
        ] = task


# ==========================================================
# ASSIGNMENT FILTER
# ==========================================================

if current_role == ROLE_COORDINATOR:

    assigned_records = [

        assignment

        for assignment in all_assignments

        if normalize(
            get_value(
                assignment,
                "Coordinator_ID",
                "Coordinator_Id"
            )
        )
        ==
        current_user_id

        and

        normalize_status(
            get_value(
                assignment,
                "Status"
            )
        )
        not in [
            "removed",
            "inactive",
            "deleted"
        ]

    ]

else:

    assigned_records = list(
        all_assignments
    )


# ==========================================================
# BUILD ASSIGNED TASK LIST
# ==========================================================

assigned_tasks = []


for assignment in assigned_records:

    task_id = normalize(
        get_value(
            assignment,
            "Task_ID",
            "Task_Id"
        )
    )


    task = task_lookup.get(
        task_id,
        {}
    )


    task_name = normalize(
        get_value(
            task,
            "Task_Name",
            "Task",
            "Name"
        )
    )


    if not task_name:

        task_name = normalize(
            get_value(
                assignment,
                "Task_Name",
                "Task"
            )
        )


    assigned_tasks.append(
        {
            "assignment": assignment,
            "task": task,
            "task_id": task_id,
            "task_name": task_name
        }
    )


# ==========================================================
# BUILD SUBMISSION LOOKUP
# ==========================================================

submission_lookup = {}


for review in all_reviews:

    status = normalize_status(
        get_value(
            review,
            "Status"
        )
    )


    if status == "deleted":

        continue


    coordinator_id = normalize(
        get_value(
            review,
            "Coordinator_ID",
            "Coordinator_Id",
            "User_ID",
            "Username"
        )
    )


    task_id = normalize(
        get_value(
            review,
            "Task_ID",
            "Task_Id"
        )
    )


    review_date = parse_date(
        get_value(
            review,
            "Date",
            "Review_Date"
        )
    )


    if (
        not coordinator_id
        or not task_id
        or not review_date
    ):

        continue


    submission_lookup[
        (
            coordinator_id,
            task_id,
            review_date
        )
    ] = review


# ==========================================================
# EXPECTED DATE GENERATOR
# ==========================================================

def expected_dates_for_assignment(
    assignment,
    task,
    period_start,
    period_end
):

    assigned_date = parse_date(
        get_value(
            assignment,
            "Assigned_Date",
            "Assignment_Date",
            "Assigned Date"
        )
    )


    due_date = parse_date(
        get_value(
            assignment,
            "Due_Date",
            "Due Date"
        )
    )


    frequency = normalize_frequency(
        get_value(
            task,
            "Frequency"
        )
    )


    if not assigned_date:

        assigned_date = period_start


    # ------------------------------------------------------
    # START DATE
    # ------------------------------------------------------

    start_date = max(
        assigned_date,
        period_start
    )


    # ------------------------------------------------------
    # END DATE
    # ------------------------------------------------------

    end_date = period_end


    if due_date:

        end_date = min(
            end_date,
            due_date
        )


    # ------------------------------------------------------
    # DO NOT CREATE FUTURE EXPECTATIONS
    # ------------------------------------------------------

    today = date.today()


    end_date = min(
        end_date,
        today
    )


    if start_date > end_date:

        return []


    result = []


    # ======================================================
    # DAILY
    # ======================================================

    if frequency == "Daily":

        current = start_date


        while current <= end_date:

            result.append(
                current
            )

            current += timedelta(
                days=1
            )


    # ======================================================
    # WEEKLY
    # ======================================================

    elif frequency == "Weekly":

        current = assigned_date


        while current < start_date:

            current += timedelta(
                days=7
            )


        while current <= end_date:

            if current >= start_date:

                result.append(
                    current
                )

            current += timedelta(
                days=7
            )


    # ======================================================
    # MONTHLY
    # ======================================================

    elif frequency == "Monthly":

        original_day = assigned_date.day

        year = start_date.year

        month = start_date.month


        while True:

            last_day = calendar.monthrange(
                year,
                month
            )[1]


            actual_day = min(
                original_day,
                last_day
            )


            current = date(
                year,
                month,
                actual_day
            )


            if (
                start_date
                <= current
                <= end_date
            ):

                result.append(
                    current
                )


            if (
                year > end_date.year
                or
                (
                    year == end_date.year
                    and
                    month >= end_date.month
                )
            ):

                break


            month += 1


            if month > 12:

                month = 1

                year += 1


    # ======================================================
    # ONE TIME
    # ======================================================

    else:

        if (
            start_date
            <= assigned_date
            <= end_date
        ):

            result.append(
                assigned_date
            )


    return result


# ==========================================================
# COORDINATOR VIEW
# ==========================================================

if current_role == ROLE_COORDINATOR:

    st.subheader(
        "📋 My Assigned Tasks"
    )


    total_tasks = len(
        assigned_tasks
    )


    completed_tasks = 0

    in_progress_tasks = 0

    pending_tasks = 0


    for item in assigned_tasks:

        status = normalize_status(
            get_value(
                item["assignment"],
                "Status"
            )
        )


        if status == "completed":

            completed_tasks += 1


        elif status in [
            "in progress",
            "inprogress"
        ]:

            in_progress_tasks += 1


        else:

            pending_tasks += 1


    completion_rate = (

        (
            completed_tasks
            /
            total_tasks
        )
        * 100

        if total_tasks > 0

        else 0

    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "📋 Assigned",
            total_tasks
        )


    with c2:

        st.metric(
            "✅ Completed",
            completed_tasks
        )


    with c3:

        st.metric(
            "🔄 In Progress",
            in_progress_tasks
        )


    with c4:

        st.metric(
            "📈 Completion",
            f"{completion_rate:.0f}%"
        )


    if total_tasks > 0:

        st.progress(
            min(
                completion_rate / 100,
                1
            )
        )


    st.caption(
        f"Overall task completion: "
        f"{completion_rate:.1f}%"
    )


    st.divider()


    # ======================================================
    # DAILY REVIEW SUBMISSION
    # ======================================================

    st.subheader(
        "📝 Submit Daily Review"
    )


    if not assigned_tasks:

        st.info(
            "No active tasks are currently assigned to you."
        )


    else:

        task_options = {}


        for index, item in enumerate(
            assigned_tasks
        ):

            assignment = item[
                "assignment"
            ]


            task_id = item[
                "task_id"
            ]


            task_name = item[
                "task_name"
            ]


            assignment_id = normalize(
                get_value(
                    assignment,
                    "Assignment_ID",
                    "Assignment_Id",
                    "ID"
                )
            )


            frequency = normalize_frequency(
                get_value(
                    item["task"],
                    "Frequency"
                )
            )


            due_date = normalize(
                get_value(
                    assignment,
                    "Due_Date",
                    "Due Date"
                )
            )


            label = (
                task_name
                or task_id
                or "Task"
            )


            if frequency:

                label = (
                    f"{label} | "
                    f"{frequency}"
                )


            if due_date:

                label = (
                    f"{label} | "
                    f"Due: {due_date}"
                )


            if assignment_id:

                label = (
                    f"{label} | "
                    f"{assignment_id}"
                )


            unique_key = (
                f"{task_id}__"
                f"{assignment_id}__"
                f"{index}"
            )


            task_options[
                unique_key
            ] = item


        selected_key = st.selectbox(
            "Select Assigned Task",
            list(
                task_options.keys()
            ),
            format_func=lambda key:
                (
                    f"{task_options[key]['task_name']}"
                    f" | "
                    f"{normalize_frequency(task_options[key]['task'].get('Frequency', ''))}"
                    f" | "
                    f"{get_value(task_options[key]['assignment'], 'Assignment_ID', 'Assignment_Id', 'ID')}"
                ),
            key="daily_review_task_selector"
        )


        selected_item = task_options[
            selected_key
        ]


        selected_assignment = (
            selected_item[
                "assignment"
            ]
        )


        selected_task = (
            selected_item[
                "task"
            ]
        )


        selected_task_id = (
            selected_item[
                "task_id"
            ]
        )


        selected_task_name = (
            selected_item[
                "task_name"
            ]
        )


        assignment_id = normalize(
            get_value(
                selected_assignment,
                "Assignment_ID",
                "Assignment_Id",
                "ID"
            )
        )


        frequency = normalize_frequency(
            get_value(
                selected_task,
                "Frequency"
            )
        )


        assigned_date = parse_date(
            get_value(
                selected_assignment,
                "Assigned_Date",
                "Assignment_Date",
                "Assigned Date"
            )
        )


        due_date = parse_date(
            get_value(
                selected_assignment,
                "Due_Date",
                "Due Date"
            )
        )


        st.info(
            f"📌 **{selected_task_name or selected_task_id}**  "
            f"| Frequency: **{frequency}**"
        )


        if assigned_date:

            st.caption(
                f"Assigned: "
                f"{assigned_date.strftime('%d-%m-%Y')}"
            )


        if due_date:

            st.caption(
                f"Due: "
                f"{due_date.strftime('%d-%m-%Y')}"
            )


        # --------------------------------------------------
        # REVIEW DATE
        # --------------------------------------------------

        review_date = st.date_input(
            "Review Date",
            value=date.today(),
            key="daily_review_date_input"
        )


        # --------------------------------------------------
        # CHECK EXPECTED DATE
        # --------------------------------------------------

        allowed_dates = []


        if assigned_date:

            allowed_dates = (
                expected_dates_for_assignment(
                    selected_assignment,
                    selected_task,
                    assigned_date,
                    date.today()
                )
            )


        date_is_expected = (
            review_date
            in allowed_dates
        )


        if allowed_dates:

            if not date_is_expected:

                st.warning(
                    "⚠️ This date is not an expected "
                    f"{frequency} submission date for this task."
                )

        else:

            st.warning(
                "⚠️ No valid submission date is available "
                "for this assignment."
            )


        # --------------------------------------------------
        # EXISTING SUBMISSION
        # --------------------------------------------------

        existing_review = (
            submission_lookup.get(
                (
                    current_user_id,
                    selected_task_id,
                    review_date
                )
            )
        )


        if existing_review:

            existing_status = normalize(
                get_value(
                    existing_review,
                    "Status"
                )
            )


            existing_remarks = normalize(
                get_value(
                    existing_review,
                    "Remarks"
                )
            )


            existing_submitted_at = normalize(
                get_value(
                    existing_review,
                    "Submitted_At",
                    "Submitted At"
                )
            )


            st.success(
                "✅ Daily Review already submitted "
                f"for {review_date.strftime('%d-%m-%Y')}."
            )


            c1, c2 = st.columns(2)


            with c1:

                st.write(
                    f"**Status:** {existing_status}"
                )


            with c2:

                st.write(
                    f"**Submitted At:** "
                    f"{existing_submitted_at or 'Not Available'}"
                )


            if existing_remarks:

                st.write(
                    f"**Remarks:** {existing_remarks}"
                )


            st.caption(
                "You can submit this task again on "
                "the next applicable submission date."
            )


        else:

            # --------------------------------------------------
            # NEW SUBMISSION
            # --------------------------------------------------

            review_status = st.selectbox(
                "Status",
                [
                    "Completed",
                    "In Progress",
                    "Pending"
                ],
                key="daily_review_status_input"
            )


            review_remarks = st.text_area(
                "Remarks / Progress Update",
                placeholder=(
                    "Enter today's work, progress, "
                    "observations or pending reason."
                ),
                height=150,
                key="daily_review_remarks_input"
            )


            submit_review = st.button(
                "✅ Submit Daily Review",
                type="primary",
                use_container_width=True,
                key="daily_review_submit_button"
            )


            if submit_review:

                review_date_text = (
                    review_date.strftime(
                        "%d-%m-%Y"
                    )
                )


                # --------------------------------------------------
                # VALIDATION
                # --------------------------------------------------

                if not selected_task_id:

                    st.error(
                        "Please select a task."
                    )

                    st.stop()


                if review_date > date.today():

                    st.error(
                        "Future date submission is not allowed."
                    )

                    st.stop()


                if assigned_date:

                    if review_date < assigned_date:

                        st.error(
                            "Review date cannot be before "
                            "the task assigned date."
                        )

                        st.stop()


                if due_date:

                    if review_date > due_date:

                        st.error(
                            "Review date cannot be after "
                            "the task due date."
                        )

                        st.stop()


                if not date_is_expected:

                    st.error(
                        f"This task is a **{frequency}** task. "
                        "Please select the correct expected "
                        "submission date."
                    )

                    st.stop()


                if (
                    review_status != "Pending"
                    and not review_remarks.strip()
                ):

                    st.error(
                        "Please enter the progress / remarks."
                    )

                    st.stop()


                # --------------------------------------------------
                # DUPLICATE CHECK
                # --------------------------------------------------

                duplicate = (
                    current_user_id,
                    selected_task_id,
                    review_date
                ) in submission_lookup


                if duplicate:

                    st.error(
                        "Daily Review for this task and "
                        "date has already been submitted."
                    )

                    st.stop()


                # --------------------------------------------------
                # SAVE
                # --------------------------------------------------

                try:

                    review_id = (
                        "REV-"
                        + uuid4().hex[:8].upper()
                    )


                    submitted_on = (
                        datetime.now().strftime(
                            "%d-%m-%Y %H:%M"
                        )
                    )


                    row = [

                        review_id,

                        review_date_text,

                        current_user_id,

                        selected_task_id,

                        assignment_id,

                        review_status,

                        review_remarks.strip(),

                        submitted_on

                    ]


                    insert_row(
                        DAILY_REVIEW,
                        row
                    )


                    # --------------------------------------------------
                    # UPDATE ASSIGNMENT STATUS
                    # --------------------------------------------------

                    assignment_row = None


                    for row_number, assignment in enumerate(
                        all_assignments,
                        start=2
                    ):

                        existing_assignment_id = normalize(
                            get_value(
                                assignment,
                                "Assignment_ID",
                                "Assignment_Id",
                                "ID"
                            )
                        )


                        if (
                            existing_assignment_id
                            == assignment_id
                        ):

                            assignment_row = (
                                row_number
                            )

                            break


                    if assignment_row:

                        update_value(
                            COORDINATOR_TASK_MAP,
                            assignment_row,
                            8,
                            review_status
                        )


                    st.success(
                        "✅ Daily Review submitted successfully."
                    )


                    st.rerun()


                except Exception as e:

                    st.error(
                        f"Unable to submit Daily Review: {e}"
                    )


    # ======================================================
    # MY REVIEW HISTORY
    # ======================================================

    st.divider()


    st.subheader(
        "📚 My Review History"
    )


    my_reviews = [

        review

        for review in all_reviews

        if normalize(
            get_value(
                review,
                "Coordinator_ID",
                "Coordinator_Id",
                "User_ID",
                "Username"
            )
        )
        ==
        current_user_id

        and

        normalize_status(
            get_value(
                review,
                "Status"
            )
        )
        != "deleted"

    ]


    if not my_reviews:

        st.info(
            "No Daily Reviews submitted yet."
        )


    else:

        history_rows = []


        for review in my_reviews:

            task_id = normalize(
                get_value(
                    review,
                    "Task_ID",
                    "Task_Id"
                )
            )


            task = task_lookup.get(
                task_id,
                {}
            )


            task_name = normalize(
                get_value(
                    task,
                    "Task_Name",
                    "Task",
                    "Name"
                )
            )


            history_rows.append(
                {

                    "Review ID":
                        get_value(
                            review,
                            "Review_ID"
                        ),

                    "Date":
                        format_date(
                            get_value(
                                review,
                                "Date",
                                "Review_Date"
                            )
                        ),

                    "Task":
                        task_name
                        or task_id,

                    "Frequency":
                        normalize_frequency(
                            get_value(
                                task,
                                "Frequency"
                            )
                        ),

                    "Status":
                        get_value(
                            review,
                            "Status"
                        ),

                    "Remarks":
                        get_value(
                            review,
                            "Remarks"
                        ),

                    "Submitted At":
                        get_value(
                            review,
                            "Submitted_At"
                        )

                }
            )


        history_df = pd.DataFrame(
            history_rows
        )


        if not history_df.empty:

            history_df = (
                history_df
                .sort_values(
                    by="Date",
                    ascending=False
                )
            )


        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )


# ==========================================================
# ADMIN / DEVELOPER MONITORING
# ==========================================================

else:

    st.subheader(
        "📊 Daily Review Monitoring"
    )


    st.caption(
        "Expected submissions are calculated from task frequency, "
        "assignment date and due date."
    )


    # ======================================================
    # DATE RANGE
    # ======================================================

    default_from = (
        date.today()
        - timedelta(
            days=6
        )
    )


    col1, col2 = st.columns(2)


    with col1:

        period_start = st.date_input(
            "From Date",
            value=default_from,
            key="monitoring_from_date"
        )


    with col2:

        period_end = st.date_input(
            "To Date",
            value=date.today(),
            key="monitoring_to_date"
        )


    if period_start > period_end:

        st.error(
            "From Date cannot be greater than To Date."
        )

        st.stop()


    # ======================================================
    # BUILD EXPECTED SUBMISSIONS
    # ======================================================

    expected_rows = []


    for assignment in all_assignments:

        assignment_status = normalize_status(
            get_value(
                assignment,
                "Status"
            )
        )


        if assignment_status in [
            "removed",
            "inactive",
            "deleted"
        ]:

            continue


        coordinator_id = normalize(
            get_value(
                assignment,
                "Coordinator_ID",
                "Coordinator_Id"
            )
        )


        task_id = normalize(
            get_value(
                assignment,
                "Task_ID",
                "Task_Id"
            )
        )


        if not coordinator_id or not task_id:

            continue


        task = task_lookup.get(
            task_id,
            {}
        )


        task_name = normalize(
            get_value(
                task,
                "Task_Name",
                "Task",
                "Name"
            )
        )


        if not task_name:

            task_name = task_id


        frequency = normalize_frequency(
            get_value(
                task,
                "Frequency"
            )
        )


        priority = normalize(
            get_value(
                task,
                "Priority"
            )
        )


        assignment_id = normalize(
            get_value(
                assignment,
                "Assignment_ID",
                "Assignment_Id",
                "ID"
            )
        )


        expected_dates = (
            expected_dates_for_assignment(
                assignment,
                task,
                period_start,
                period_end
            )
        )


        for expected_date in expected_dates:

            key = (
                coordinator_id,
                task_id,
                expected_date
            )


            submitted_review = (
                submission_lookup.get(
                    key
                )
            )


            if submitted_review:

                submission_status = "Submitted"

                actual_status = normalize(
                    get_value(
                        submitted_review,
                        "Status"
                    )
                )


                remarks = normalize(
                    get_value(
                        submitted_review,
                        "Remarks"
                    )
                )


                submitted_at = normalize(
                    get_value(
                        submitted_review,
                        "Submitted_At"
                    )
                )

            else:

                submission_status = "Missing"

                actual_status = ""

                remarks = ""

                submitted_at = ""


            expected_rows.append(
                {

                    "Date":
                        expected_date.strftime(
                            "%d-%m-%Y"
                        ),

                    "Coordinator":
                        coordinator_id,

                    "Task ID":
                        task_id,

                    "Task":
                        task_name,

                    "Frequency":
                        frequency,

                    "Priority":
                        priority,

                    "Assignment ID":
                        assignment_id,

                    "Submission":
                        submission_status,

                    "Status":
                        actual_status,

                    "Remarks":
                        remarks,

                    "Submitted At":
                        submitted_at

                }
            )


    # ======================================================
    # FILTER OPTIONS
    # ======================================================

    coordinator_options = sorted(
        list(
            dict.fromkeys(
                row[
                    "Coordinator"
                ]

                for row in expected_rows

                if row[
                    "Coordinator"
                ]
            )
        )
    )


    task_options = sorted(
        list(
            dict.fromkeys(
                row[
                    "Task ID"
                ]

                for row in expected_rows

                if row[
                    "Task ID"
                ]
            )
        )
    )


    filter1, filter2 = st.columns(2)


    with filter1:

        selected_coordinator = st.selectbox(
            "Coordinator",
            ["All"] + coordinator_options,
            key="monitoring_coordinator_filter"
        )


    with filter2:

        selected_task = st.selectbox(
            "Task",
            ["All"] + task_options,
            key="monitoring_task_filter"
        )


    # ======================================================
    # APPLY FILTERS
    # ======================================================

    filtered_rows = list(
        expected_rows
    )


    if selected_coordinator != "All":

        filtered_rows = [

            row

            for row in filtered_rows

            if row[
                "Coordinator"
            ]
            ==
            selected_coordinator

        ]


    if selected_task != "All":

        filtered_rows = [

            row

            for row in filtered_rows

            if row[
                "Task ID"
            ]
            ==
            selected_task

        ]


    # ======================================================
    # MAIN METRICS
    # ======================================================

    expected_count = len(
        filtered_rows
    )


    submitted_count = sum(

        1

        for row in filtered_rows

        if row[
            "Submission"
        ]
        ==
        "Submitted"

    )


    missing_count = (

        expected_count
        -
        submitted_count

    )


    completion_percentage = (

        (
            submitted_count
            /
            expected_count
        )
        * 100

        if expected_count

        else 0

    )


    st.divider()


    st.subheader(
        "📈 Expected vs Submitted"
    )


    m1, m2, m3, m4 = st.columns(4)


    with m1:

        st.metric(
            "📅 Expected",
            expected_count
        )


    with m2:

        st.metric(
            "✅ Submitted",
            submitted_count
        )


    with m3:

        st.metric(
            "⚠️ Missing",
            missing_count
        )


    with m4:

        st.metric(
            "📊 Completion",
            f"{completion_percentage:.1f}%"
        )


    if expected_count > 0:

        st.progress(
            min(
                completion_percentage / 100,
                1
            )
        )


    # ======================================================
    # MISSING SUBMISSIONS
    # ======================================================

    st.divider()


    st.subheader(
        "⚠️ Missing Submissions"
    )


    missing_rows = [

        row

        for row in filtered_rows

        if row[
            "Submission"
        ]
        ==
        "Missing"

    ]


    if missing_rows:

        missing_df = pd.DataFrame(
            missing_rows
        )


        st.dataframe(
            missing_df,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.success(
            "🎉 No missing submissions for the selected period."
        )


    # ======================================================
    # DATE-WISE MONITORING
    # ======================================================

    st.divider()


    st.subheader(
        "📋 Date-wise Submission Monitoring"
    )


    if filtered_rows:

        monitoring_df = pd.DataFrame(
            filtered_rows
        )


        st.dataframe(
            monitoring_df,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "No expected submissions found "
            "for the selected period."
        )


    # ======================================================
    # COORDINATOR-WISE SUMMARY
    # ======================================================

    st.divider()


    st.subheader(
        "👨‍⚕️ Coordinator-wise Summary"
    )


    coordinator_summary = {}


    for row in filtered_rows:

        coordinator = row[
            "Coordinator"
        ]


        if coordinator not in coordinator_summary:

            coordinator_summary[
                coordinator
            ] = {

                "Expected": 0,

                "Submitted": 0,

                "Missing": 0

            }


        coordinator_summary[
            coordinator
        ]["Expected"] += 1


        if row[
            "Submission"
        ] == "Submitted":

            coordinator_summary[
                coordinator
            ]["Submitted"] += 1

        else:

            coordinator_summary[
                coordinator
            ]["Missing"] += 1


    summary_rows = []


    for coordinator, values in (
        coordinator_summary.items()
    ):

        expected = values[
            "Expected"
        ]


        submitted = values[
            "Submitted"
        ]


        missing = values[
            "Missing"
        ]


        completion = (

            (
                submitted
                /
                expected
            )
            * 100

            if expected

            else 0

        )


        summary_rows.append(
            {

                "Coordinator":
                    coordinator,

                "Expected":
                    expected,

                "Submitted":
                    submitted,

                "Missing":
                    missing,

                "Completion %":
                    round(
                        completion,
                        1
                    )

            }
        )


    if summary_rows:

        summary_df = pd.DataFrame(
            summary_rows
        )


        summary_df = (
            summary_df
            .sort_values(
                by="Completion %",
                ascending=False
            )
        )


        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "No coordinator monitoring data available."
        )


    # ======================================================
    # ACTUAL SUBMITTED REVIEWS
    # ======================================================

    st.divider()


    st.subheader(
        "📝 Submitted Review Records"
    )


    submitted_reviews = [

        row

        for row in all_reviews

        if normalize_status(
            get_value(
                row,
                "Status"
            )
        )
        != "deleted"

    ]


    # ------------------------------------------------------
    # DATE FILTER
    # ------------------------------------------------------

    filtered_submitted_reviews = []


    for review in submitted_reviews:

        review_date = parse_date(
            get_value(
                review,
                "Date",
                "Review_Date"
            )
        )


        if not review_date:

            continue


        if (
            period_start
            <= review_date
            <= period_end
        ):

            filtered_submitted_reviews.append(
                review
            )


    # ------------------------------------------------------
    # COORDINATOR FILTER
    # ------------------------------------------------------

    if selected_coordinator != "All":

        filtered_submitted_reviews = [

            row

            for row in filtered_submitted_reviews

            if normalize(
                get_value(
                    row,
                    "Coordinator_ID",
                    "Coordinator_Id",
                    "User_ID",
                    "Username"
                )
            )
            ==
            selected_coordinator

        ]


    # ------------------------------------------------------
    # TASK FILTER
    # ------------------------------------------------------

    if selected_task != "All":

        filtered_submitted_reviews = [

            row

            for row in filtered_submitted_reviews

            if normalize(
                get_value(
                    row,
                    "Task_ID",
                    "Task_Id"
                )
            )
            ==
            selected_task

        ]


    if filtered_submitted_reviews:

        review_display_rows = []


        for review in filtered_submitted_reviews:

            task_id = normalize(
                get_value(
                    review,
                    "Task_ID",
                    "Task_Id"
                )
            )


            task = task_lookup.get(
                task_id,
                {}
            )


            task_name = normalize(
                get_value(
                    task,
                    "Task_Name",
                    "Task",
                    "Name"
                )
            )


            if not task_name:

                task_name = task_id


            review_display_rows.append(
                {

                    "Date":
                        format_date(
                            get_value(
                                review,
                                "Date",
                                "Review_Date"
                            )
                        ),

                    "Coordinator":
                        get_value(
                            review,
                            "Coordinator_ID",
                            "Coordinator_Id",
                            "User_ID",
                            "Username"
                        ),

                    "Task ID":
                        task_id,

                    "Task":
                        task_name,

                    "Status":
                        get_value(
                            review,
                            "Status"
                        ),

                    "Remarks":
                        get_value(
                            review,
                            "Remarks"
                        ),

                    "Submitted At":
                        get_value(
                            review,
                            "Submitted_At"
                        )

                }
            )


        st.dataframe(
            pd.DataFrame(
                review_display_rows
            ),
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "No submitted review records found "
            "for the selected period."
        )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "MSU / EPID Health Coordinator Monitoring System | "
    "Daily Review Monitoring"
)
