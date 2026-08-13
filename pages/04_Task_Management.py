import streamlit as st
from datetime import date

from config.config import (
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR,
    COORDINATOR_MASTER,
    TASK_MASTER,
)

from utils.google_sheet import read_all
from services.task_assignment_service import TaskAssignmentService


st.set_page_config(
    page_title="Task Management",
    page_icon="📋",
    layout="wide"
)


# ============================================================
# SESSION CHECK
# ============================================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

current_user = st.session_state.get("user", {})

current_role = str(
    current_user.get("Role", "")
).strip()

current_user_id = str(
    current_user.get("User_ID", "")
).strip()


# ============================================================
# HEADER
# ============================================================

st.title("📋 Task Management")

st.caption(
    f"User: {current_user.get('Username', '')} | "
    f"Role: {current_role}"
)

st.divider()


# ============================================================
# LOAD DATA
# ============================================================

try:
    coordinators = read_all(COORDINATOR_MASTER)
except Exception:
    coordinators = []

try:
    tasks = read_all(TASK_MASTER)
except Exception:
    tasks = []

try:
    assignments = TaskAssignmentService.get_all_assignments()
except Exception:
    assignments = []


# ============================================================
# NORMALIZE ACTIVE COORDINATORS
# ============================================================

active_coordinators = []

for coordinator in coordinators:

    status = str(
        coordinator.get("Status", "ACTIVE")
    ).strip().upper()

    if status != "ACTIVE":
        continue

    active_coordinators.append(coordinator)


# ============================================================
# NORMALIZE ACTIVE TASKS
# ============================================================

active_tasks = []

for task in tasks:

    status = str(
        task.get("Status", "ACTIVE")
    ).strip().upper()

    if status != "ACTIVE":
        continue

    active_tasks.append(task)


# ============================================================
# ACCESS CONTROL
# ============================================================

if current_role not in [
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR
]:

    st.error("You do not have permission to access Task Management.")
    st.stop()


# ============================================================
# SUMMARY
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Tasks",
        len(active_tasks)
    )

with col2:
    st.metric(
        "Active Coordinators",
        len(active_coordinators)
    )

with col3:
    st.metric(
        "Total Assignments",
        len(assignments)
    )

pending_count = sum(
    1
    for x in assignments
    if str(
        x.get("Status", "")
    ).strip().upper() == "PENDING"
)

with col4:
    st.metric(
        "Pending Assignments",
        pending_count
    )


st.divider()


# ============================================================
# DEVELOPER / ADMIN ASSIGNMENT SECTION
# ============================================================

if current_role in [
    ROLE_DEVELOPER,
    ROLE_ADMIN
]:

    st.subheader("➕ Assign Task")

    if not active_coordinators:

        st.warning("No active coordinators found.")

    elif not active_tasks:

        st.warning("No active tasks found.")

    else:

        coordinator_options = {}

        for coordinator in active_coordinators:

            coordinator_id = str(
                coordinator.get(
                    "Coordinator_ID",
                    coordinator.get("User_ID", "")
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

            if coordinator_id:
                coordinator_options[
                    f"{coordinator_name} ({coordinator_id})"
                ] = coordinator_id


        task_options = {}

        for task in active_tasks:

            task_id = str(
                task.get("Task_ID", "")
            ).strip()

            task_name = str(
                task.get(
                    "Task_Name",
                    task.get(
                        "Task",
                        task_id
                    )
                )
            ).strip()

            if task_id:

                task_options[
                    f"{task_name} ({task_id})"
                ] = task_id


        selected_coordinator_label = st.selectbox(
            "Select Coordinator",
            list(coordinator_options.keys()),
            key="task_management_coordinator"
        )

        selected_task_label = st.selectbox(
            "Select Task",
            list(task_options.keys()),
            key="task_management_task"
        )

        col1, col2, col3 = st.columns(3)

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

        with col3:

            priority = st.selectbox(
                "Priority",
                [
                    "Low",
                    "Medium",
                    "High",
                    "Urgent"
                ],
                index=1,
                key="task_priority"
            )

        remarks = st.text_area(
            "Remarks",
            key="task_assignment_remarks"
        )

        if st.button(
            "➕ Assign Task",
            type="primary",
            use_container_width=True,
            key="assign_task_button"
        ):

            selected_coordinator_id = coordinator_options[
                selected_coordinator_label
            ]

            selected_task_id = task_options[
                selected_task_label
            ]

            if due_date < assigned_date:

                st.error(
                    "Due Date cannot be earlier than Assigned Date."
                )

            else:

                success, message = (
                    TaskAssignmentService.assign_task(
                        coordinator_id=selected_coordinator_id,
                        task_id=selected_task_id,
                        assigned_by=current_user_id,
                        assigned_date=assigned_date.strftime(
                            "%d-%m-%Y"
                        ),
                        due_date=due_date.strftime(
                            "%d-%m-%Y"
                        ),
                        priority=priority,
                        remarks=remarks
                    )
                )

                if success:

                    st.success(message)

                    st.cache_data.clear()

                    st.rerun()

                else:

                    st.error(message)


    st.divider()


# ============================================================
# COORDINATOR VIEW
# ============================================================

if current_role == ROLE_COORDINATOR:

    st.subheader("📌 My Assigned Tasks")

    my_assignments = (
        TaskAssignmentService.coordinator_tasks(
            current_user_id
        )
    )

    if not my_assignments:

        st.info(
            "No tasks have been assigned to you."
        )

    else:

        for index, assignment in enumerate(
            my_assignments
        ):

            task_id = str(
                assignment.get(
                    "Task_ID",
                    ""
                )
            ).strip()

            task_name = task_id

            for task in active_tasks:

                if str(
                    task.get("Task_ID", "")
                ).strip() == task_id:

                    task_name = str(
                        task.get(
                            "Task_Name",
                            task.get(
                                "Task",
                                task_id
                            )
                        )
                    )

                    break


            status = str(
                assignment.get(
                    "Status",
                    "Pending"
                )
            ).strip()

            priority = str(
                assignment.get(
                    "Priority",
                    "Medium"
                )
            ).strip()

            due_date = str(
                assignment.get(
                    "Due_Date",
                    ""
                )
            ).strip()

            assignment_id = str(
                assignment.get(
                    "Assignment_ID",
                    ""
                )
            ).strip()


            with st.container(
                border=True
            ):

                col1, col2, col3 = st.columns(
                    [4, 2, 2]
                )

                with col1:

                    st.markdown(
                        f"### 📋 {task_name}"
                    )

                    st.caption(
                        f"Assignment ID: {assignment_id}"
                    )

                with col2:

                    st.write(
                        f"**Priority:** {priority}"
                    )

                with col3:

                    st.write(
                        f"**Due Date:** {due_date}"
                    )

                st.write(
                    f"**Current Status:** {status}"
                )

                if status.upper() != "COMPLETED":

                    if st.button(
                        "✅ Submit / Mark Completed",
                        key=f"complete_task_{assignment_id}_{index}",
                        use_container_width=True
                    ):

                        # Find the actual Google Sheet row.
                        all_assignments = (
                            TaskAssignmentService
                            .get_all_assignments()
                        )

                        target_row = None

                        for row_number, item in enumerate(
                            all_assignments,
                            start=2
                        ):

                            if str(
                                item.get(
                                    "Assignment_ID",
                                    ""
                                )
                            ).strip() == assignment_id:

                                target_row = row_number
                                break

                        if target_row is None:

                            st.error(
                                "Assignment could not be found."
                            )

                        else:

                            success = (
                                TaskAssignmentService
                                .update_status(
                                    target_row,
                                    "Completed"
                                )
                            )

                            if success:

                                st.success(
                                    "Task submitted successfully."
                                )

                                st.cache_data.clear()

                                st.rerun()


# ============================================================
# ADMIN / DEVELOPER ASSIGNMENT MONITOR
# ============================================================

if current_role in [
    ROLE_DEVELOPER,
    ROLE_ADMIN
]:

    st.subheader("📊 Assignment Monitoring")

    if not assignments:

        st.info(
            "No task assignments available."
        )

    else:

        display_rows = []

        for assignment in assignments:

            coordinator_id = str(
                assignment.get(
                    "Coordinator_ID",
                    ""
                )
            ).strip()

            task_id = str(
                assignment.get(
                    "Task_ID",
                    ""
                )
            ).strip()

            coordinator_name = coordinator_id

            for coordinator in active_coordinators:

                cid = str(
                    coordinator.get(
                        "Coordinator_ID",
                        coordinator.get(
                            "User_ID",
                            ""
                        )
                    )
                ).strip()

                if cid == coordinator_id:

                    coordinator_name = str(
                        coordinator.get(
                            "Coordinator_Name",
                            coordinator.get(
                                "Full_Name",
                                coordinator_id
                            )
                        )
                    )

                    break


            task_name = task_id

            for task in active_tasks:

                tid = str(
                    task.get(
                        "Task_ID",
                        ""
                    )
                ).strip()

                if tid == task_id:

                    task_name = str(
                        task.get(
                            "Task_Name",
                            task.get(
                                "Task",
                                task_id
                            )
                        )
                    )

                    break


            display_rows.append(
                {
                    "Assignment ID": assignment.get(
                        "Assignment_ID",
                        ""
                    ),
                    "Coordinator": coordinator_name,
                    "Task": task_name,
                    "Assigned Date": assignment.get(
                        "Assigned_Date",
                        ""
                    ),
                    "Due Date": assignment.get(
                        "Due_Date",
                        ""
                    ),
                    "Priority": assignment.get(
                        "Priority",
                        ""
                    ),
                    "Status": assignment.get(
                        "Status",
                        ""
                    ),
                    "Remarks": assignment.get(
                        "Remarks",
                        ""
                    )
                }
            )


        st.dataframe(
            display_rows,
            use_container_width=True,
            hide_index=True
        )
