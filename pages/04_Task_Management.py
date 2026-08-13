# pages/04_Task_Management.py

import streamlit as st

from core.navigation import require_login
from services.task_service import TaskService
from services.task_assignment_service import TaskAssignmentService
from services.coordinator_service import CoordinatorService


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Task Management",
    page_icon="📋",
    layout="wide"
)

require_login(["Developer", "Admin"])


# ==========================================================
# SESSION
# ==========================================================

current_username = str(
    st.session_state.get(
        "username",
        "SYSTEM"
    )
).strip()

current_role = str(
    st.session_state.get(
        "role",
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
# LOAD DATA
# ==========================================================

try:
    tasks = TaskService.get_all_tasks()
except Exception:
    tasks = []

if tasks is None:
    tasks = []


try:
    coordinators = CoordinatorService.get_all_coordinators()
except Exception:
    coordinators = []

if coordinators is None:
    coordinators = []


# ==========================================================
# NORMALIZE DATA
# ==========================================================

def get_value(record, *keys):

    for key in keys:

        value = record.get(key, "")

        if value is not None and str(value).strip():

            return value

    return ""


# ==========================================================
# DASHBOARD COUNTS
# ==========================================================

total_tasks = len(tasks)

active_tasks = sum(
    1
    for task in tasks
    if str(
        get_value(
            task,
            "Status",
            "Task_Status"
        )
    ).strip().upper()
    == "ACTIVE"
)

inactive_tasks = sum(
    1
    for task in tasks
    if str(
        get_value(
            task,
            "Status",
            "Task_Status"
        )
    ).strip().upper()
    in [
        "INACTIVE",
        "DISABLED"
    ]
)


# ==========================================================
# DASHBOARD CARDS
# ==========================================================

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "📋 Total Tasks",
        total_tasks
    )

with c2:

    st.metric(
        "🟢 Active Tasks",
        active_tasks
    )

with c3:

    st.metric(
        "🔴 Inactive Tasks",
        inactive_tasks
    )

st.divider()


# ==========================================================
# TABS
# ==========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📋 Task List",
        "➕ Create Task",
        "👥 Assign Tasks"
    ]
)


# ==========================================================
# TAB 1 — TASK LIST
# ==========================================================

with tab1:

    st.subheader("📋 All Tasks")

    if not tasks:

        st.info(
            "No tasks found."
        )

    else:

        search = st.text_input(
            "🔍 Search Task",
            key="task_search"
        )

        status_filter = st.selectbox(
            "Status",
            [
                "All",
                "ACTIVE",
                "INACTIVE",
                "DISABLED"
            ],
            key="task_status_filter"
        )

        filtered_tasks = tasks

        if search.strip():

            search_text = (
                search
                .strip()
                .lower()
            )

            filtered_tasks = [

                task

                for task in filtered_tasks

                if (

                    search_text
                    in str(
                        get_value(
                            task,
                            "Task_ID",
                            "Task_Id",
                            "ID"
                        )
                    ).lower()

                    or

                    search_text
                    in str(
                        get_value(
                            task,
                            "Task_Name",
                            "Task",
                            "Name"
                        )
                    ).lower()

                    or

                    search_text
                    in str(
                        get_value(
                            task,
                            "Description"
                        )
                    ).lower()

                )
            ]

        if status_filter != "All":

            filtered_tasks = [

                task

                for task in filtered_tasks

                if str(
                    get_value(
                        task,
                        "Status",
                        "Task_Status"
                    )
                ).strip().upper()
                == status_filter

            ]

        st.dataframe(
            filtered_tasks,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Showing {len(filtered_tasks)} "
            f"of {len(tasks)} tasks"
        )


# ==========================================================
# TAB 2 — CREATE TASK
# ==========================================================

with tab2:

    st.subheader("➕ Create New Task")

    task_name = st.text_input(
        "Task Name",
        key="create_task_name"
    )

    description = st.text_area(
        "Task Description",
        key="create_task_description"
    )

    frequency = st.selectbox(
        "Frequency",
        [
            "Daily",
            "Weekly",
            "Monthly",
            "One Time"
        ],
        key="create_task_frequency"
    )

    priority = st.selectbox(
        "Priority",
        [
            "High",
            "Medium",
            "Low"
        ],
        key="create_task_priority"
    )

    task_status = st.selectbox(
        "Status",
        [
            "ACTIVE",
            "INACTIVE"
        ],
        key="create_task_status"
    )

    if st.button(
        "✅ Create Task",
        use_container_width=True,
        key="create_task_button"
    ):

        if not task_name.strip():

            st.error(
                "Task Name is required."
            )

        else:

            try:

                result = TaskService.create_task(
                    task_name=task_name.strip(),
                    description=description.strip(),
                    frequency=frequency,
                    priority=priority,
                    status=task_status,
                    created_by=current_username
                )

                if isinstance(result, tuple):

                    ok, message = result

                else:

                    ok = bool(result)
                    message = (
                        "Task created successfully."
                        if ok
                        else "Unable to create task."
                    )

                if ok:

                    st.success(message)

                    st.rerun()

                else:

                    st.error(message)

            except TypeError:

                try:

                    result = TaskService.create_task(
                        task_name.strip(),
                        description.strip(),
                        frequency,
                        priority,
                        task_status,
                        current_username
                    )

                    if isinstance(result, tuple):

                        ok, message = result

                    else:

                        ok = bool(result)
                        message = (
                            "Task created successfully."
                            if ok
                            else "Unable to create task."
                        )

                    if ok:

                        st.success(message)

                        st.rerun()

                    else:

                        st.error(message)

                except Exception as e:

                    st.error(
                        f"Unable to create task: {e}"
                    )

            except Exception as e:

                st.error(
                    f"Unable to create task: {e}"
                )


# ==========================================================
# TAB 3 — ASSIGN TASKS
# ==========================================================

with tab3:

    st.subheader(
        "👥 Assign Tasks to Coordinators"
    )

    if not tasks:

        st.warning(
            "No tasks available for assignment."
        )

    elif not coordinators:

        st.warning(
            "No coordinators found."
        )

    else:

        # --------------------------------------------------
        # COORDINATOR SELECTION
        # --------------------------------------------------

        coordinator_labels = []

        for coordinator in coordinators:

            coordinator_id = get_value(
                coordinator,
                "Coordinator_ID",
                "Coordinator_Id",
                "User_ID",
                "Username",
                "ID"
            )

            coordinator_name = get_value(
                coordinator,
                "Full_Name",
                "Coordinator_Name",
                "Name",
                "Username"
            )

            if coordinator_id:

                if coordinator_name:

                    coordinator_labels.append(
                        (
                            coordinator_id,
                            f"{coordinator_name} "
                            f"({coordinator_id})"
                        )
                    )

                else:

                    coordinator_labels.append(
                        (
                            coordinator_id,
                            str(coordinator_id)
                        )
                    )

        if not coordinator_labels:

            st.warning(
                "No valid coordinators found."
            )

        else:

            coordinator_ids = [
                item[0]
                for item in coordinator_labels
            ]

            coordinator_display = {
                item[0]: item[1]
                for item in coordinator_labels
            }

            selected_coordinator = st.selectbox(

                "Select Coordinator",

                coordinator_ids,

                format_func=lambda x:
                coordinator_display.get(
                    x,
                    str(x)
                ),

                key="selected_coordinator"

            )

            st.divider()

            # --------------------------------------------------
            # TASK SELECTION
            # --------------------------------------------------

            task_labels = []

            for task in tasks:

                task_id = get_value(
                    task,
                    "Task_ID",
                    "Task_Id",
                    "ID"
                )

                task_name_value = get_value(
                    task,
                    "Task_Name",
                    "Task",
                    "Name"
                )

                task_status_value = str(
                    get_value(
                        task,
                        "Status",
                        "Task_Status"
                    )
                ).strip().upper()

                if (
                    task_id
                    and task_status_value
                    not in [
                        "INACTIVE",
                        "DISABLED",
                        "DELETED"
                    ]
                ):

                    label = (
                        f"{task_name_value} "
                        f"({task_id})"
                    )

                    task_labels.append(
                        (
                            task_id,
                            label
                        )
                    )

            if not task_labels:

                st.warning(
                    "No active tasks available."
                )

            else:

                task_ids = [
                    item[0]
                    for item in task_labels
                ]

                task_display = {
                    item[0]: item[1]
                    for item in task_labels
                }

                selected_tasks = st.multiselect(

                    "Select Task(s)",

                    task_ids,

                    format_func=lambda x:
                    task_display.get(
                        x,
                        str(x)
                    ),

                    key="selected_tasks"

                )

                st.divider()

                if st.button(
                    "➕ Assign Selected Task(s)",
                    use_container_width=True,
                    key="assign_tasks_button"
                ):

                    if not selected_tasks:

                        st.warning(
                            "Please select at least one task."
                        )

                    else:

                        success_count = 0
                        error_messages = []

                        for task_id in selected_tasks:

                            try:

                                result = (
                                    TaskAssignmentService
                                    .assign_task(
                                        coordinator_id=selected_coordinator,
                                        task_id=task_id,
                                        assigned_by=current_username
                                    )
                                )

                                if isinstance(
                                    result,
                                    tuple
                                ):

                                    ok, message = result

                                else:

                                    ok = bool(result)
                                    message = (
                                        "Task assigned."
                                        if ok
                                        else "Assignment failed."
                                    )

                                if ok:

                                    success_count += 1

                                else:

                                    error_messages.append(
                                        str(message)
                                    )

                            except TypeError:

                                try:

                                    result = (
                                        TaskAssignmentService
                                        .assign_task(
                                            selected_coordinator,
                                            task_id,
                                            current_username
                                        )
                                    )

                                    if isinstance(
                                        result,
                                        tuple
                                    ):

                                        ok, message = result

                                    else:

                                        ok = bool(result)
                                        message = (
                                            "Task assigned."
                                            if ok
                                            else "Assignment failed."
                                        )

                                    if ok:

                                        success_count += 1

                                    else:

                                        error_messages.append(
                                            str(message)
                                        )

                                except Exception as e:

                                    error_messages.append(
                                        str(e)
                                    )

                            except Exception as e:

                                error_messages.append(
                                    str(e)
                                )

                        if success_count > 0:

                            st.success(
                                f"✅ {success_count} "
                                f"task(s) assigned successfully."
                            )

                        for message in error_messages:

                            st.warning(message)

                        if success_count > 0:

                            st.rerun()

            # --------------------------------------------------
            # CURRENT ASSIGNMENTS
            # --------------------------------------------------

            st.divider()

            st.subheader(
                "📌 Current Assignments"
            )

            try:

                assignments = (
                    TaskAssignmentService
                    .get_coordinator_tasks(
                        selected_coordinator
                    )
                )

            except Exception:

                assignments = []

            if assignments is None:

                assignments = []

            if not assignments:

                st.info(
                    "No tasks currently assigned "
                    "to this coordinator."
                )

            else:

                assignment_rows = []

                for assignment in assignments:

                    assignment_rows.append(
                        assignment
                    )

                st.dataframe(
                    assignment_rows,
                    use_container_width=True,
                    hide_index=True
                )

                st.divider()

                st.subheader(
                    "🗑 Remove Task Assignment"
                )

                assignment_options = []

                for assignment in assignments:

                    assignment_task_id = get_value(
                        assignment,
                        "Task_ID",
                        "Task_Id",
                        "ID"
                    )

                    assignment_task_name = get_value(
                        assignment,
                        "Task_Name",
                        "Task",
                        "Name"
                    )

                    if assignment_task_id:

                        assignment_options.append(
                            (
                                assignment_task_id,
                                f"{assignment_task_name} "
                                f"({assignment_task_id})"
                            )
                        )

                if assignment_options:

                    remove_task_id = st.selectbox(

                        "Select Assigned Task",

                        [
                            item[0]
                            for item in assignment_options
                        ],

                        format_func=lambda x: next(
                            (
                                item[1]
                                for item
                                in assignment_options
                                if item[0] == x
                            ),
                            str(x)
                        ),

                        key="remove_task_id"

                    )

                    if st.button(
                        "🗑 Remove Assignment",
                        use_container_width=True,
                        key="remove_assignment_button"
                    ):

                        try:

                            result = (
                                TaskAssignmentService
                                .remove_assignment(
                                    coordinator_id=selected_coordinator,
                                    task_id=remove_task_id,
                                    modified_by=current_username
                                )
                            )

                            if isinstance(
                                result,
                                tuple
                            ):

                                ok, message = result

                            else:

                                ok = bool(result)
                                message = (
                                    "Assignment removed."
                                    if ok
                                    else "Unable to remove assignment."
                                )

                            if ok:

                                st.success(message)

                                st.rerun()

                            else:

                                st.error(message)

                        except TypeError:

                            try:

                                result = (
                                    TaskAssignmentService
                                    .remove_assignment(
                                        selected_coordinator,
                                        remove_task_id,
                                        current_username
                                    )
                                )

                                if isinstance(
                                    result,
                                    tuple
                                ):

                                    ok, message = result

                                else:

                                    ok = bool(result)
                                    message = (
                                        "Assignment removed."
                                        if ok
                                        else "Unable to remove assignment."
                                    )

                                if ok:

                                    st.success(message)

                                    st.rerun()

                                else:

                                    st.error(message)

                            except Exception as e:

                                st.error(
                                    f"Unable to remove assignment: {e}"
                                )

                        except Exception as e:

                            st.error(
                                f"Unable to remove assignment: {e}"
                            )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "MSU / EPID Health Coordinator Monitoring System "
    "| Task Management"
)
