import streamlit as st

from core.navigation import require_login

from config.config import (
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="System Manual",
    page_icon="📖",
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

current_username = str(
    st.session_state.get(
        "username",
        ""
    )
).strip()


# ==========================================================
# HEADER
# ==========================================================

st.title("📖 System Manual")

st.caption(
    f"User: {current_username} | Role: {current_role}"
)

st.divider()


# ==========================================================
# INTRODUCTION
# ==========================================================

st.subheader("🎯 About the System")

st.markdown(
    """
    The **Coordinator Monitoring & Task Management System** is designed
    to manage users, assign tasks, collect Daily Reviews and monitor
    Coordinator-level performance from a single portal.

    The system follows a role-based access structure:

    **Developer → Admin → Coordinator**
    """
)


# ==========================================================
# SYSTEM FLOW
# ==========================================================

st.subheader("🔄 System Workflow")

st.markdown(
    """
    ### Overall Workflow

    **1. User Management**

    Developer / Admin creates and manages authorised users.

    ↓

    **2. Task Management**

    Developer / Admin assigns tasks to Coordinators.

    ↓

    **3. Task Execution**

    Coordinator works on assigned tasks.

    ↓

    **4. Daily Review**

    Coordinator submits daily status and progress.

    ↓

    **5. Monitoring**

    Admin / Developer monitors completion and pending work.

    ↓

    **6. Dashboard**

    Management can review overall performance.
    """
)


# ==========================================================
# DEVELOPER
# ==========================================================

with st.expander(
    "👨‍💻 Developer Manual",
    expanded=current_role.lower() == "developer"
):

    st.markdown(
        """
        ## Developer

        Developer has the highest level of system access.

        ### User Management

        Developer can:

        - Create Admin users
        - Create Coordinator users
        - Change Admin passwords
        - Change Coordinator passwords
        - Enable users
        - Disable users
        - Monitor user accounts

        ### Task Management

        Developer can:

        - View available tasks
        - Assign tasks
        - Select Coordinator
        - Set due dates
        - Set priority
        - Add assignment remarks
        - Monitor task assignments

        ### Daily Review

        Developer can:

        - View submitted Daily Reviews
        - View Coordinator-wise performance
        - Check Pending reviews
        - Check In Progress reviews
        - Check Completed reviews
        - Monitor completion percentage

        ### System Settings

        Developer can access system-level settings and
        application controls.
        """
    )


# ==========================================================
# ADMIN
# ==========================================================

with st.expander(
    "🧑‍💼 Admin Manual",
    expanded=current_role.lower() == "admin"
):

    st.markdown(
        """
        ## Admin

        Admin manages operational activities.

        ### User Management

        Admin can:

        - Create Coordinator users
        - Change Coordinator passwords
        - Enable Coordinator accounts
        - Disable Coordinator accounts

        Admin cannot manage Developer accounts.

        Admin cannot change Developer passwords.

        ### Task Management

        Admin can:

        - View tasks
        - Assign tasks to Coordinators
        - Set task priority
        - Set assigned date
        - Set due date
        - Add remarks

        ### Daily Review

        Admin can:

        - Monitor submitted reviews
        - View Coordinator-wise progress
        - Check task completion
        - Identify pending work
        """
    )


# ==========================================================
# COORDINATOR
# ==========================================================

with st.expander(
    "👨‍⚕️ Coordinator Manual",
    expanded=current_role.lower() == "coordinator"
):

    st.markdown(
        """
        ## Coordinator

        Coordinator is responsible for completing assigned work
        and submitting Daily Reviews.

        ### Step 1 — Check Tasks

        Open:

        **Task Management**

        Review:

        - Task name
        - Assigned date
        - Due date
        - Priority
        - Current status

        ### Step 2 — Complete Work

        Work on the assigned task according to the required
        priority and due date.

        ### Step 3 — Submit Daily Review

        Open:

        **Daily Review**

        Select:

        - Assigned Task
        - Review Date
        - Status

        Enter:

        - Progress update
        - Remarks
        - Pending reason, if applicable

        Then click:

        **Submit Daily Review**

        ### Step 4 — Review History

        Previously submitted Daily Reviews can be viewed
        from the Daily Review page.
        """
    )


# ==========================================================
# DAILY REVIEW
# ==========================================================

st.subheader("📝 Daily Review Process")

st.markdown(
    """
    ### Status meanings

    **Pending**

    The assigned task has not yet been completed.

    **In Progress**

    Work has started and is currently continuing.

    **Completed**

    The assigned work has been completed.

    ### Recommended Daily Review

    Every Coordinator should submit a Daily Review for active
    assigned tasks according to the organisation's review process.

    The review should contain meaningful progress information
    rather than only a status.
    """
)


# ==========================================================
# TASK MANAGEMENT
# ==========================================================

st.subheader("📋 Task Management Process")

st.markdown(
    """
    ### Assigning a Task

    1. Open **Task Management**
    2. Select **Assign Task**
    3. Select Coordinator
    4. Select Task
    5. Enter Assigned Date
    6. Enter Due Date
    7. Select Priority
    8. Add Remarks if required
    9. Click **Assign Task**

    The assignment becomes available to the selected Coordinator.
    """
)


# ==========================================================
# USER MANAGEMENT
# ==========================================================

st.subheader("👥 User Management Rules")

st.markdown(
    """
    | Action | Developer | Admin | Coordinator |
    |---|---|---|---|
    | Manage Developer | ✅ | ❌ | ❌ |
    | Manage Admin | ✅ | ❌ | ❌ |
    | Manage Coordinator | ✅ | ✅ | ❌ |
    | Change Admin Password | ✅ | ❌ | ❌ |
    | Change Coordinator Password | ✅ | ✅ | ❌ |
    | Assign Tasks | ✅ | ✅ | ❌ |
    | Submit Daily Review | ❌ | ❌ | ✅ |
    | Monitor Daily Reviews | ✅ | ✅ | ❌ |
    """
)


# ==========================================================
# TROUBLESHOOTING
# ==========================================================

st.subheader("🛠️ Troubleshooting")

with st.expander(
    "Task is not visible to Coordinator"
):

    st.markdown(
        """
        Check:

        1. Correct Coordinator was selected.
        2. Correct Task was selected.
        3. Assignment was successfully saved.
        4. Assignment has not been removed or disabled.
        5. Coordinator is logged in with the correct account.
        """
    )


with st.expander(
    "Daily Review shows no tasks"
):

    st.markdown(
        """
        The Coordinator must have an active task assignment.

        Check the assignment from:

        **Task Management → Coordinator Assignments**
        """
    )


with st.expander(
    "Password change is not available"
):

    st.markdown(
        """
        Password-management permissions are role based.

        Developer can manage Admin and Coordinator accounts.

        Admin can manage Coordinator accounts only.

        Coordinator cannot manage other accounts.
        """
    )


with st.expander(
    "Daily Review submission fails"
):

    st.markdown(
        """
        Check:

        - Task is assigned to the logged-in Coordinator.
        - Task assignment is active.
        - Review date is selected.
        - Status is selected.
        - Progress / remarks are entered when required.

        If the problem continues, capture the error message and
        share it with the system Developer.
        """
    )


# ==========================================================
# SECURITY
# ==========================================================

st.subheader("🔐 Basic Security Rules")

st.markdown(
    """
    - Do not share your username or password.
    - Do not use another person's account.
    - Log out after completing work on a shared computer.
    - Administrators should disable inactive user accounts.
    - Passwords should not be shared through public messages.
    - Only authorised users should access the portal.
    """
)


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "System Manual • Coordinator Monitoring & Task Management System"
)
