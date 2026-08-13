import streamlit as st
import pandas as pd
from datetime import date

from core.navigation import require_login

from services.task_assignment_service import TaskAssignmentService
from services.task_service import TaskService

from utils.google_sheet import read_all

from config.config import (
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR,
    USERS
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Task Management",
    page_icon="📋",
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

current_role = str(
    st.session_state.get(
        "role",
        ""
    )
).strip()

current_user_id = str(
    st.session_state.get(
        "user_id",
        ""
    )
).strip()

current_username = str(
    st.session_state.get(
        "username",
        ""
    )
).strip()


# ==========================================================
# HEADER
# ==========================================================

st.title("📋 Task Management")

st.caption(
    f"User: {current_username} | Role: {current_role}"
)

st.divider()


# ==========================================================
# HELPERS
# ==========================================================

def value(record, *keys):

    if not record:
        return ""

    for key in keys:

        v = record.get(
            key,
            ""
        )

        if (
            v is not None
            and str(v).strip() != ""
        ):
            return str(v).strip()

    return ""


def normalize(value_text):

    return str(
        value_text
        if value_text is not None
        else ""
    ).strip()


# ==========================================================
# LOAD TASKS
# ==========================================================

try:

    tasks = TaskService.get_all_tasks()

except Exception:

    tasks = []

tasks = tasks or []


# ==========================================================
# LOAD ASSIGNMENTS
# ==========================================================

try:

    assignments = (
        TaskAssignmentService
        .get_all_assignments()
    )

except Exception:

    assignments = []

assignments = assignments or []


# ==========================================================
# LOAD USERS
# ==========================================================

try:

    users = read_all(
        USERS
    )

except Exception:

    users = []

users = users or []


# ==========================================================
# COORDINATORS
# ==========================================================

coordinators = [

    user

    for user in users

    if normalize(
        value(
            user,
            "Role"
        )
    ).lower()
    == "coordinator"

    and normalize(
        value(
            user,
            "Status"
        )
    ).upper()
    not in [
        "DISABLED",
        "INACTIVE",
        "DELETED"
    ]

]


# ==========================================================
# TASK LOOKUP
# ==========================================================

task_lookup = {}

for task in tasks:

    task_id = normalize(
        value(
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
# ASSIGNMENT COUNTS
# ==========================================================

active_assignments = [

    assignment

    for assignment in assignments

    if normalize(
        value(
            assignment,
            "Status"
        )
    ).lower()

    not in [
        "removed",
        "inactive",
        "deleted"
    ]

]


total_tasks = len(
    tasks
)

total_assignments = len(
    active_assignments
)

pending_assignments = sum(

    1

    for assignment in active_assignments

    if normalize(
        value(
            assignment,
            "Status"
        )
    ).lower()
    == "pending"

)

completed_assignments = sum(

    1

    for assignment in active_assignments

    if normalize(
        value(
            assignment,
            "Status"
        )
    ).lower()
    == "completed"

)


# ==========================================================
# METRICS
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "📋 Total Tasks",
        total_tasks
    )

with c2:

    st.metric(
        "👨‍⚕️ Coordinators",
        len(coordinators)
    )

with c3:

    st.metric(
        "📌 Active Assignments",
        total_assignments
    )

with c4:

    st.metric(
        "⏳ Pending",
        pending_assignments
    )


st.divider()


# ==========================================================
# COORDINATOR VIEW
# ==========================================================

if current_role == ROLE_COORDINATOR:

    st.subheader(
        "📋 My Assigned Tasks"
    )

    my_assignments = [

        assignment

        for assignment in active_assignments

        if normalize(
            value(
                assignment,
                "Coordinator_ID",
                "Coordinator_Id"
            )
        )
        == current_user_id

    ]


    if not my_assignments:

        st.info(
            "No tasks have been assigned to you."
        )

    else:

        rows = []

        for assignment in my_assignments:

            task_id = normalize(
                value(
                    assignment,
                    "Task_ID",
                    "Task_Id"
                )
            )

            task = task_lookup.get(
                task_id,
                {}
            )

            rows.append(
                {
                    "Assignment ID":
                        value(
                            assignment,
                            "Assignment_ID",
                            "Assignment_Id"
                        ),

                    "Task":
                        value(
                            task,
                            "Task_Name",
                            "Task",
                            "Name"
                        ) or task_id,

                    "Assigned Date":
                        value(
                            assignment,
                            "Assigned_Date",
                            "Assigned Date"
                        ),

                    "Due Date":
                        value(
                            assignment,
                            "Due_Date",
                            "Due Date"
                        ),

                    "Priority":
                        value(
                            assignment,
                            "Priority"
                        ),

                    "Status":
                        value(
                            assignment,
                            "Status"
                        ),

                    "Remarks":
                        value(
                            assignment,
                            "Remarks"
                        )
                }
            )


        st.dataframe(
            pd.DataFrame(
                rows
            ),
            use_container_width=True,
            hide_index=True
        )


# ==========================================================
# ADMIN / DEVELOPER MANAGEMENT
# ==========================================================

else:

    tab1, tab2, tab3 = st.tabs(
        [
            "📋 All Tasks",
            "➕ Assign Task",
            "👨‍⚕️ Coordinator Assignments"
        ]
    )


    # ======================================================
    # ALL TASKS
    # ======================================================

    with tab1:

        st.subheader(
            "📋 Task Master"
        )


        if not tasks:

            st.info(
                "No tasks available."
            )

        else:

            task_rows = []

            for task in tasks:

                task_id = value(
                    task,
                    "Task_ID",
                    "Task_Id",
                    "ID"
                )

                task_rows.append(
                    {
                        "Task ID":
                            task_id,

                        "Task Name":
                            value(
                                task,
                                "Task_Name",
                                "Task",
                                "Name"
                            ),

                        "Description":
                            value(
                                task,
                                "Description",
                                "Task_Description"
                            ),

                        "Frequency":
                            value(
                                task,
                                "Frequency"
                            ),

                        "Priority":
                            value(
                                task,
                                "Priority"
                            ),

                        "Status":
                            value(
                                task,
                                "Status"
                            )
                    }
                )


            st.dataframe(
                pd.DataFrame(
                    task_rows
                ),
                use_container_width=True,
                hide_index=True
            )


    # ======================================================
    # ASSIGN TASK
    # ======================================================

    with tab2:

        st.subheader(
            "➕ Assign Task to Coordinator"
        )


        if not tasks:

            st.warning(
                "No tasks are available for assignment."
            )

        elif not coordinators:

            st.warning(
                "No active coordinators found."
            )

        else:

            coordinator_map = {}

            for coordinator in coordinators:

                coordinator_id = value(
                    coordinator,
                    "User_ID",
                    "User_Id",
                    "ID"
                )

                coordinator_name = value(
                    coordinator,
                    "Full_Name",
                    "Username",
                    "User_ID"
                )

                coordinator_map[
                    coordinator_id
                ] = (
                    f"{coordinator_name} "
                    f"({coordinator_id})"
                )


            task_map = {}

            for task in tasks:

                task_id = value(
                    task,
                    "Task_ID",
                    "Task_Id",
                    "ID"
                )

                task_name = value(
                    task,
                    "Task_Name",
                    "Task",
                    "Name"
                )

                task_map[
                    task_id
                ] = (
                    f"{task_name} "
                    f"({task_id})"
                )


            selected_coordinator = st.selectbox(
                "Select Coordinator",
                list(
                    coordinator_map.keys()
                ),
                format_func=lambda x:
                    coordinator_map[x],
                key="assign_coordinator"
            )


            selected_task = st.selectbox(
                "Select Task",
                list(
                    task_map.keys()
                ),
                format_func=lambda x:
                    task_map[x],
                key="assign_task"
            )


            col1, col2 = st.columns(2)


            with col1:

                assigned_date = st.date_input(
                    "Assigned Date",
                    value=date.today(),
                    key="assigned_date"
                )


            with col2:

                due_date = st.date_input(
                    "Due Date",
                    value=date.today(),
                    key="due_date"
                )


            priority = st.selectbox(
                "Priority",
                [
                    "Low",
                    "Medium",
                    "High",
                    "Critical"
                ],
                index=1,
                key="task_priority"
            )


            remarks = st.text_area(
                "Remarks",
                key="assignment_remarks",
                height=100
            )


            assign_button = st.button(
                "➕ Assign Task",
                type="primary",
                use_container_width=True,
                key="assign_task_button"
            )


            if assign_button:

                if due_date < assigned_date:

                    st.error(
                        "Due Date cannot be before Assigned Date."
                    )

                else:

                    duplicate = False

                    for assignment in active_assignments:

                        existing_coordinator = normalize(
                            value(
                                assignment,
                                "Coordinator_ID",
                                "Coordinator_Id"
                            )
                        )

                        existing_task = normalize(
                            value(
                                assignment,
                                "Task_ID",
                                "Task_Id"
                            )
                        )

                        if (

                            existing_coordinator
                            == selected_coordinator

                            and

                            existing_task
                            == selected_task

                        ):

                            duplicate = True

                            break


                    if duplicate:

                        st.warning(
                            "This task is already assigned "
                            "to this coordinator."
                        )

                    else:

                        try:

                            success, message = (
                                TaskAssignmentService
                                .assign_task(
                                    coordinator_id=
                                        selected_coordinator,

                                    task_id=
                                        selected_task,

                                    assigned_by=
                                        current_username,

                                    assigned_date=
                                        assigned_date.strftime(
                                            "%d-%m-%Y"
                                        ),

                                    due_date=
                                        due_date.strftime(
                                            "%d-%m-%Y"
                                        ),

                                    priority=
                                        priority,

                                    remarks=
                                        remarks.strip()
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


                        except Exception as e:

                            st.error(
                                f"Unable to assign task: {e}"
                            )


    # ======================================================
    # COORDINATOR ASSIGNMENTS
    # ======================================================

    with tab3:

        st.subheader(
            "👨‍⚕️ Coordinator Assignments"
        )


        if not active_assignments:

            st.info(
                "No active task assignments."
            )

        else:

            assignment_rows = []

            for assignment in active_assignments:

                coordinator_id = value(
                    assignment,
                    "Coordinator_ID",
                    "Coordinator_Id"
                )

                task_id = value(
                    assignment,
                    "Task_ID",
                    "Task_Id"
                )

                coordinator_name = coordinator_id

                for coordinator in coordinators:

                    cid = value(
                        coordinator,
                        "User_ID",
                        "User_Id",
                        "ID"
                    )

                    if cid == coordinator_id:

                        coordinator_name = value(
                            coordinator,
                            "Full_Name",
                            "Username"
                        ) or coordinator_id

                        break


                task_name = value(
                    task_lookup.get(
                        task_id,
                        {}
                    ),
                    "Task_Name",
                    "Task",
                    "Name"
                ) or task_id


                assignment_rows.append(
                    {
                        "Assignment ID":
                            value(
                                assignment,
                                "Assignment_ID",
                                "Assignment_Id"
                            ),

                        "Coordinator":
                            coordinator_name,

                        "Coordinator ID":
                            coordinator_id,

                        "Task":
                            task_name,

                        "Assigned Date":
                            value(
                                assignment,
                                "Assigned_Date"
                            ),

                        "Due Date":
                            value(
                                assignment,
                                "Due_Date"
                            ),

                        "Priority":
                            value(
                                assignment,
                                "Priority"
                            ),

                        "Status":
                            value(
                                assignment,
                                "Status"
                            ),

                        "Remarks":
                            value(
                                assignment,
                                "Remarks"
                            )
                    }
                )


            st.dataframe(
                pd.DataFrame(
                    assignment_rows
                ),
                use_container_width=True,
                hide_index=True
            )
