import streamlit as st

from config.config import (
    APP_NAME,
    APP_VERSION,
    APP_OWNER,
    APP_ENVIRONMENT,
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="System Manual",
    page_icon="📖",
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
# HEADER
# ==========================================================

st.title(
    "📖 System Manual"
)

st.caption(
    f"{APP_NAME} | Version {APP_VERSION}"
)

st.divider()


# ==========================================================
# SYSTEM OVERVIEW
# ==========================================================

st.header(
    "🏥 1. System Overview"
)

st.write(
    """
    The MSU / EPID Health Coordinator Monitoring System
    is designed to manage Coordinator activities, task
    assignments, Daily Reviews and administrative monitoring
    through a centralized dashboard.
    """
)

st.info(
    f"""
    **Application:** {APP_NAME}

    **Version:** {APP_VERSION}

    **Owner:** {APP_OWNER}

    **Environment:** {APP_ENVIRONMENT}
    """
)


# ==========================================================
# LOGIN
# ==========================================================

st.header(
    "🔐 2. Login"
)

with st.expander(
    "How to Login",
    expanded=True
):

    st.markdown(
        """
        1. Enter your registered **Username**.
        2. Enter your **Password**.
        3. Click **Login**.
        4. After successful authentication, the system
           redirects you to the dashboard available for
           your role.

        The system validates:

        - Username
        - Password
        - Account Status
        - Account Lock Status
        - Login Attempts
        """
    )


# ==========================================================
# ROLES
# ==========================================================

st.header(
    "👤 3. User Roles"
)


role_data = [

    {
        "Role": "Developer",
        "Main Access": (
            "Full system monitoring and management"
        ),
        "Password Management": (
            "Admin + Coordinator"
        ),
        "Task Management": (
            "Full"
        ),
        "Daily Review": (
            "Full monitoring"
        )
    },

    {
        "Role": "Admin",
        "Main Access": (
            "Administrative monitoring"
        ),
        "Password Management": (
            "Coordinator"
        ),
        "Task Management": (
            "Full"
        ),
        "Daily Review": (
            "Monitoring"
        )
    },

    {
        "Role": "Coordinator",
        "Main Access": (
            "Assigned work management"
        ),
        "Password Management": (
            "No"
        ),
        "Task Management": (
            "Assigned tasks"
        ),
        "Daily Review": (
            "Own task submission"
        )
    }

]


st.dataframe(
    role_data,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# DEVELOPER
# ==========================================================

if current_role == ROLE_DEVELOPER:

    st.header(
        "🛠️ 4. Developer Guide"
    )

    with st.expander(
        "User Management"
    ):

        st.markdown(
            """
            Developer can manage passwords for:

            - Admin users
            - Coordinator users

            Developer cannot change another Developer's
            password through the User Management interface.
            """
        )


    with st.expander(
        "Task Management"
    ):

        st.markdown(
            """
            Developer can:

            - View active Coordinators
            - View active Tasks
            - Assign Tasks
            - Set Assigned Date
            - Set Due Date
            - Set Priority
            - Add Remarks
            - Monitor assignment status
            """
        )


    with st.expander(
        "Daily Review Monitoring"
    ):

        st.markdown(
            """
            Developer can monitor Daily Reviews submitted
            by Coordinators.

            The monitoring includes:

            - Total Reviews
            - Completed Reviews
            - Pending Reviews
            - In Progress Reviews
            """
        )


    with st.expander(
        "Developer Dashboard"
    ):

        st.markdown(
            """
            The Developer Dashboard provides an overall
            system-level view of:

            - Active Users
            - Active Coordinators
            - Active Tasks
            - Pending Assignments
            - Completed Assignments
            - Daily Reviews
            - Coordinator-wise Task Progress
            """
        )


# ==========================================================
# ADMIN
# ==========================================================

if current_role == ROLE_ADMIN:

    st.header(
        "👨‍💼 5. Admin Guide"
    )

    with st.expander(
        "User Management"
    ):

        st.markdown(
            """
            Admin can change passwords for Coordinator
            accounts.

            Admin cannot change:

            - Developer passwords
            - Admin passwords
            """
        )


    with st.expander(
        "Task Management"
    ):

        st.markdown(
            """
            Admin can assign tasks to active Coordinators.

            While assigning a task, Admin can specify:

            - Coordinator
            - Task
            - Assigned Date
            - Due Date
            - Priority
            - Remarks
            """
        )


    with st.expander(
        "Daily Review Monitoring"
    ):

        st.markdown(
            """
            Admin can monitor Daily Review activity across
            Coordinators.

            The dashboard displays task and review progress.
            """
        )


# ==========================================================
# COORDINATOR
# ==========================================================

if current_role == ROLE_COORDINATOR:

    st.header(
        "👨‍⚕️ 6. Coordinator Guide"
    )

    with st.expander(
        "Assigned Tasks"
    ):

        st.markdown(
            """
            Coordinators can view the tasks assigned to them.

            Each assignment may contain:

            - Task Name
            - Assignment ID
            - Assigned Date
            - Due Date
            - Priority
            - Status
            - Remarks
            """
        )


    with st.expander(
        "Submitting Daily Review"
    ):

        st.markdown(
            """
            To submit a Daily Review:

            1. Select the assigned task.
            2. Select the Review Date.
            3. Select the current Status.
            4. Enter Progress / Remarks.
            5. Click **Submit Daily Review**.

            The system records the review and updates the
            corresponding task assignment status.
            """
        )


    with st.expander(
        "Task Completion"
    ):

        st.markdown(
            """
            When a Coordinator submits a task as Completed,
            the assignment status is updated to Completed.

            The Dashboard then updates the overall completion
            percentage.
            """
        )


# ==========================================================
# TASK WORKFLOW
# ==========================================================

st.header(
    "📋 7. Task Workflow"
)

st.markdown(
    """
    **Task Master**

    ↓

    **Developer / Admin assigns Task**

    ↓

    **Task appears in Coordinator Dashboard**

    ↓

    **Coordinator performs Task**

    ↓

    **Coordinator submits Daily Review**

    ↓

    **Assignment Status Updated**

    ↓

    **Admin / Developer monitors progress**
    """
)


# ==========================================================
# DAILY REVIEW WORKFLOW
# ==========================================================

st.header(
    "📝 8. Daily Review Workflow"
)

st.markdown(
    """
    **Assigned Task**

    ↓

    **Coordinator selects Task**

    ↓

    **Select Review Date**

    ↓

    **Select Status**

    ↓

    **Enter Progress / Remarks**

    ↓

    **Submit Daily Review**

    ↓

    **Review stored in Daily Review sheet**

    ↓

    **Task Assignment status updated**
    """
)


# ==========================================================
# STATUS DEFINITIONS
# ==========================================================

st.header(
    "📊 9. Status Definitions"
)

status_data = [

    {
        "Status": "Pending",
        "Meaning": "Task has not yet been completed."
    },

    {
        "Status": "In Progress",
        "Meaning": "Coordinator is currently working on the task."
    },

    {
        "Status": "Completed",
        "Meaning": "Coordinator has completed and submitted the task."
    }

]


st.dataframe(
    status_data,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# SECURITY
# ==========================================================

st.header(
    "🔒 10. Security"
)

st.markdown(
    """
    The application uses role-based access control.

    Passwords are stored using password hashes rather than
    plain-text passwords.

    Login attempts are tracked.

    Accounts can become locked after repeated failed
    authentication attempts.

    Password reset by authorized users also resets login
    attempts and unlocks the account.
    """
)


# ==========================================================
# TROUBLESHOOTING
# ==========================================================

st.header(
    "🛠️ 11. Troubleshooting"
)

with st.expander(
    "I cannot see my assigned task"
):

    st.write(
        "Confirm that the task has been assigned to your "
        "Coordinator ID and that the assignment is active."
    )


with st.expander(
    "I cannot submit Daily Review"
):

    st.write(
        "Confirm that at least one active task has been "
        "assigned to your Coordinator account."
    )


with st.expander(
    "My account is locked"
):

    st.write(
        "Contact an authorized Developer or Administrator "
        "for account assistance."
    )


with st.expander(
    "My dashboard is empty"
):

    st.write(
        "Dashboard information depends on the records stored "
        "in the connected Google Sheets."
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    f"{APP_NAME} | "
    f"Version {APP_VERSION} | "
    f"{APP_OWNER}"
)
