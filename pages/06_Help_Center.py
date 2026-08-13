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
    page_title="Help Center",
    page_icon="🆘",
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

st.title("🆘 Help Center")

st.caption(
    f"User: {current_username} | Role: {current_role}"
)

st.divider()


# ==========================================================
# QUICK HELP
# ==========================================================

st.subheader("🚀 Quick Help")

c1, c2, c3 = st.columns(3)


with c1:

    st.markdown(
        """
        ### 👥 User Management

        **Developer**
        - Create Admin users
        - Create Coordinator users
        - Change Admin passwords
        - Change Coordinator passwords
        - Enable / disable users

        **Admin**
        - Create Coordinator users
        - Change Coordinator passwords
        - Enable / disable Coordinators
        """
    )


with c2:

    st.markdown(
        """
        ### 📋 Task Management

        **Developer / Admin**
        - View all tasks
        - Assign tasks to Coordinators
        - Set assigned date
        - Set due date
        - Set priority
        - Add assignment remarks

        **Coordinator**
        - View assigned tasks
        - Track task status
        - Submit Daily Review
        """
    )


with c3:

    st.markdown(
        """
        ### 📝 Daily Review

        **Coordinator**
        1. Open Daily Review
        2. Select assigned task
        3. Select review date
        4. Select status
        5. Enter progress / remarks
        6. Click **Submit Daily Review**

        **Admin / Developer**
        - Monitor all submitted reviews
        - View Coordinator-wise progress
        - Check completion percentage
        """
    )


st.divider()


# ==========================================================
# ROLE BASED GUIDE
# ==========================================================

st.subheader("🎯 Role-wise Guide")


if current_role.lower() == "developer":

    with st.expander(
        "👨‍💻 Developer Guide",
        expanded=True
    ):

        st.markdown(
            """
            ### Developer

            The Developer has the highest system-management access.

            **Main responsibilities**

            - Manage Admin accounts
            - Manage Coordinator accounts
            - Reset passwords
            - Enable / disable users
            - Monitor task assignments
            - Monitor Daily Reviews
            - Check overall system activity

            **Recommended workflow**

            `User Management`
            → `Task Management`
            → `Daily Review`
            → `Developer Dashboard`
            """ 
        )


elif current_role.lower() == "admin":

    with st.expander(
        "🧑‍💼 Admin Guide",
        expanded=True
    ):

        st.markdown(
            """
            ### Admin

            Admin manages operational users and daily work.

            **Main responsibilities**

            - Manage Coordinators
            - Reset Coordinator passwords
            - Enable / disable Coordinators
            - Assign tasks
            - Monitor Daily Reviews
            - Review Coordinator performance

            **Recommended workflow**

            `User Management`
            → `Task Management`
            → `Daily Review`
            → `Admin Dashboard`
            """
        )


elif current_role.lower() == "coordinator":

    with st.expander(
        "👨‍⚕️ Coordinator Guide",
        expanded=True
    ):

        st.markdown(
            """
            ### Coordinator

            Coordinator is responsible for completing assigned work
            and submitting daily progress.

            **Daily workflow**

            1. Open **Task Management**
            2. Check assigned tasks
            3. Complete / work on assigned task
            4. Open **Daily Review**
            5. Select the task
            6. Select the current status
            7. Enter progress / remarks
            8. Click **Submit Daily Review**

            The submitted review becomes visible to Admin
            and Developer monitoring dashboards.
            """
        )


st.divider()


# ==========================================================
# STATUS DEFINITIONS
# ==========================================================

st.subheader("📊 Status Definitions")

status_data = {
    "Status": [
        "Pending",
        "In Progress",
        "Completed",
        "Disabled"
    ],
    "Meaning": [
        "Task has been assigned but work has not started.",
        "Task is currently being worked on.",
        "Task has been completed and submitted.",
        "User account is temporarily inactive."
    ]
}

st.table(
    status_data
)


st.divider()


# ==========================================================
# FREQUENTLY ASKED QUESTIONS
# ==========================================================

st.subheader("❓ Frequently Asked Questions")


with st.expander(
    "Why can't a Coordinator see a task?"
):

    st.write(
        """
        Check whether the task has been assigned to the correct
        Coordinator from **Task Management → Assign Task**.
        """
    )


with st.expander(
    "Why can't a Coordinator submit Daily Review?"
):

    st.write(
        """
        A Daily Review can be submitted only for an active task
        assigned to the logged-in Coordinator.

        Check:

        - Coordinator ID
        - Task ID
        - Assignment status
        - Active assignment
        """
    )


with st.expander(
    "Can Admin change a Developer password?"
):

    st.write(
        """
        No.

        Developer accounts are controlled by the Developer role.

        Admin can manage Coordinator accounts.
        """
    )


with st.expander(
    "Can Developer change Admin and Coordinator passwords?"
):

    st.write(
        """
        Yes.

        Developer has the highest user-management permission
        in the system.
        """
    )


with st.expander(
    "What happens after a Coordinator submits Daily Review?"
):

    st.write(
        """
        The review is stored in the Daily Review data source and
        becomes available for Admin / Developer monitoring.

        The related assignment status is also updated.
        """
    )


with st.expander(
    "How is the completion percentage calculated?"
):

    st.write(
        """
        Completion percentage is calculated from completed reviews
        compared with the total submitted reviews.
        """
    )


st.divider()


# ==========================================================
# SUPPORT
# ==========================================================

st.subheader("📞 Support")

st.info(
    """
    If an unexpected error occurs:

    1. Note the page name.
    2. Note the logged-in role.
    3. Take a screenshot of the error.
    4. Share the error message with the system Developer.
    """
)


st.caption(
    "Coordinator Monitoring & Task Management System"
)
