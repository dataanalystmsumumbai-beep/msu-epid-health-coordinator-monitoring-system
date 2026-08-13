import streamlit as st

from config.config import (
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR,
    APP_NAME,
    APP_VERSION,
    APP_OWNER,
    APP_ENVIRONMENT
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Help Center",
    page_icon="❓",
    layout="wide"
)


# ==========================================================
# LOGIN CHECK
# ==========================================================

if (
    "logged_in" not in st.session_state
    or not st.session_state.logged_in
):

    st.error(
        "Please login first."
    )

    st.stop()


# ==========================================================
# USER
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
    "❓ Help Center"
)

st.caption(
    "MSU / EPID Health Coordinator Monitoring System"
)

st.divider()


# ==========================================================
# SYSTEM INFORMATION
# ==========================================================

st.subheader(
    "ℹ️ System Information"
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Application",
        APP_NAME
    )

with c2:

    st.metric(
        "Version",
        APP_VERSION
    )

with c3:

    st.metric(
        "Owner",
        APP_OWNER
    )

with c4:

    st.metric(
        "Environment",
        APP_ENVIRONMENT
    )


st.divider()


# ==========================================================
# ROLE BASED HELP
# ==========================================================

st.subheader(
    "👤 Your Role"
)

st.info(
    f"You are logged in as **{current_role}**."
)


# ==========================================================
# COORDINATOR
# ==========================================================

if current_role == ROLE_COORDINATOR:

    with st.expander(
        "📋 How to manage assigned tasks",
        expanded=True
    ):

        st.markdown(
            """
            1. Open **Task Management**.
            2. Review your assigned tasks.
            3. Check the priority and due date.
            4. Complete the assigned work.
            5. Submit the task as completed.
            """
        )


    with st.expander(
        "📝 How to submit Daily Review"
    ):

        st.markdown(
            """
            1. Open **Daily Review**.
            2. Select the assigned task.
            3. Select the review date.
            4. Select the current status.
            5. Enter your progress / remarks.
            6. Click **Submit Daily Review**.
            """
        )


    with st.expander(
        "📊 Understanding your progress"
    ):

        st.markdown(
            """
            - **Assigned** = Total tasks assigned to you.
            - **Completed** = Tasks submitted as completed.
            - **Pending** = Tasks not yet completed.
            - **Progress** = Completed tasks as a percentage of assigned tasks.
            """
        )


# ==========================================================
# ADMIN
# ==========================================================

elif current_role == ROLE_ADMIN:

    with st.expander(
        "👥 User Management"
    ):

        st.markdown(
            """
            As an Admin you can manage **Coordinator**
            account passwords.

            You cannot change Developer or Admin passwords.
            """
        )


    with st.expander(
        "📋 Task Management"
    ):

        st.markdown(
            """
            As an Admin you can:

            - View active tasks
            - View active Coordinators
            - Assign tasks to Coordinators
            - Set due dates
            - Set priority
            - Add assignment remarks
            - Monitor task assignments
            """
        )


    with st.expander(
        "📊 Daily Review"
    ):

        st.markdown(
            """
            Daily Review allows Admin users to monitor:

            - Total submitted reviews
            - Completed reviews
            - Pending reviews
            - In-progress reviews
            - Coordinator review activity
            """
        )


# ==========================================================
# DEVELOPER
# ==========================================================

elif current_role == ROLE_DEVELOPER:

    with st.expander(
        "🛠️ Developer Responsibilities"
    ):

        st.markdown(
            """
            Developer users have the highest application-level
            management access.

            Developer can manage:

            - Admin passwords
            - Coordinator passwords
            - Task assignments
            - System monitoring
            - Daily Review monitoring
            """
        )


    with st.expander(
        "🔐 Password Management"
    ):

        st.markdown(
            """
            Developer can reset passwords for:

            - Admin
            - Coordinator

            Password reset also resets failed login attempts
            and unlocks the selected account.
            """
        )


    with st.expander(
        "📊 Monitoring"
    ):

        st.markdown(
            """
            Developer can monitor task assignments and
            Daily Review submissions across the system.
            """
        )


# ==========================================================
# GENERAL FAQ
# ==========================================================

st.divider()

st.subheader(
    "❓ Frequently Asked Questions"
)


with st.expander(
    "Why can't I see a task?"
):

    st.write(
        "A task must be assigned to your Coordinator account "
        "before it appears in your assigned task list."
    )


with st.expander(
    "Why can't I submit the same Daily Review twice?"
):

    st.write(
        "The system prevents duplicate Daily Review "
        "submissions for the same user, task and date."
    )


with st.expander(
    "What happens when I submit a task as Completed?"
):

    st.write(
        "The corresponding task assignment status is updated "
        "to Completed."
    )


with st.expander(
    "What happens if my account is locked?"
):

    st.write(
        "After repeated failed password attempts, an account "
        "can become locked. An authorized Developer or Admin "
        "can reset the account according to their permissions."
    )


with st.expander(
    "Who can change passwords?"
):

    st.write(
        "Developer can manage Admin and Coordinator passwords. "
        "Admin can manage Coordinator passwords."
    )


# ==========================================================
# CONTACT / SYSTEM NOTE
# ==========================================================

st.divider()

st.subheader(
    "📞 Support"
)

st.info(
    "For system configuration, database or application-level "
    "issues, contact the authorized MSU / EPID system administrator."
)


st.caption(
    f"{APP_NAME} | Version {APP_VERSION}"
)
