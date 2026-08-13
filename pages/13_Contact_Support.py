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
    page_title="Contact Support",
    page_icon="📞",
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

st.title("📞 Contact Support")

st.caption(
    f"User: {current_username} | Role: {current_role}"
)

st.divider()


# ==========================================================
# SUPPORT INTRODUCTION
# ==========================================================

st.subheader("🆘 Need Help?")

st.markdown(
    """
    If you are facing an issue with the portal, first check the
    **Help Center** and **System Manual**.

    If the issue continues, record the following information before
    contacting the system Developer:

    - Page where the issue occurred
    - Logged-in username
    - User role
    - Task ID / Assignment ID, if applicable
    - Date and time of the issue
    - Exact error message
    - Screenshot of the issue
    """
)


st.divider()


# ==========================================================
# COMMON ISSUES
# ==========================================================

st.subheader("🔧 Common Issues")


with st.expander(
    "🔐 Login problem"
):

    st.write(
        """
        Check that the username and password are correct.

        If the account has been disabled, contact the authorised
        Developer / Admin responsible for user management.
        """
    )


with st.expander(
    "📋 Task is not visible"
):

    st.write(
        """
        Check whether the task has actually been assigned to the
        logged-in Coordinator.

        Also verify the Coordinator ID and Task ID.
        """
    )


with st.expander(
    "📝 Daily Review cannot be submitted"
):

    st.write(
        """
        Check:

        1. The task is assigned to the logged-in Coordinator.
        2. The assignment is active.
        3. Review date is selected.
        4. Status is selected.
        5. Required progress / remarks are entered.
        """
    )


with st.expander(
    "👥 Cannot change a user's password"
):

    st.write(
        """
        Password-management access is role based.

        Developer:
        Can manage Admin and Coordinator passwords.

        Admin:
        Can manage Coordinator passwords.

        Coordinator:
        Cannot manage other users.
        """
    )


with st.expander(
    "📊 Dashboard does not show updated data"
):

    st.write(
        """
        Refresh the page first.

        If the data is still not updated, verify that the underlying
        task assignment or Daily Review was successfully submitted.
        """
    )


st.divider()


# ==========================================================
# SUPPORT REQUEST
# ==========================================================

st.subheader("✉️ Report an Issue")

with st.form(
    "support_request_form"
):

    issue_type = st.selectbox(
        "Issue Type",
        [
            "Login / Authentication",
            "User Management",
            "Task Management",
            "Daily Review",
            "Notifications",
            "Reports Dashboard",
            "Other"
        ]
    )


    issue_subject = st.text_input(
        "Issue Subject"
    )


    issue_description = st.text_area(
        "Describe the Issue",
        height=150,
        placeholder=(
            "Describe what happened, what you expected, "
            "and any error message shown."
        )
    )


    reference_id = st.text_input(
        "Task / Assignment / Review ID (if applicable)"
    )


    submitted = st.form_submit_button(
        "📨 Submit Support Request",
        type="primary",
        use_container_width=True
    )


    if submitted:

        if not issue_subject.strip():

            st.error(
                "Please enter an issue subject."
            )

        elif not issue_description.strip():

            st.error(
                "Please describe the issue."
            )

        else:

            st.success(
                """
                Support request details have been captured.

                Please share the issue details and screenshot with
                the system Developer / authorised support person.
                """
            )


st.divider()


# ==========================================================
# SUPPORT CHECKLIST
# ==========================================================

st.subheader("✅ Before Reporting an Issue")

checklist = [
    "Refresh the page.",
    "Confirm that you are logged into the correct account.",
    "Check whether your role has permission for the requested action.",
    "Verify the Task ID / Assignment ID if applicable.",
    "Check the Help Center.",
    "Check the System Manual.",
    "Take a screenshot if the problem continues."
]

for item in checklist:

    st.checkbox(
        item,
        key=f"support_check_{item}"
    )


st.divider()


# ==========================================================
# SECURITY NOTICE
# ==========================================================

st.warning(
    """
    **Security Notice**

    Never include passwords, authentication secrets, API keys,
    or other confidential credentials in a support request or screenshot.
    """
)


# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "Contact Support • Coordinator Monitoring & Task Management System"
)
