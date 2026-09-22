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
# ACCESS CONTROL
# ==========================================================

require_login([
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR
])


# ==========================================================
# SESSION INFORMATION
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

current_user_id = str(
    st.session_state.get(
        "user_id",
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
# PRIMARY SUPPORT CONTACT
# ==========================================================

st.subheader("👨‍💻 Need Technical Support?")

st.success(
    """
    If you experience a technical issue with this portal,
    please **contact the Data Analyst / designated system support person**.
    """
)

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown("### 👤 Support Person")

    st.write(
        "**Data Analyst**"
    )

with c2:

    st.markdown("### 🖥️ Support Area")

    st.write(
        "System / Portal Support"
    )

with c3:

    st.markdown("### 📋 Information Required")

    st.write(
        "Issue details + screenshot"
    )


st.info(
    """
    **Recommended:** Before contacting the Data Analyst,
    first check the **Help Center** and **System Manual**.
    If the issue continues, share the issue details and screenshot
    with the Data Analyst.
    """
)


st.divider()


# ==========================================================
# INFORMATION TO SHARE
# ==========================================================

st.subheader("📋 Information to Share with the Data Analyst")

st.markdown(
    """
    When reporting an issue, provide the following information:

    - **Page name** where the issue occurred
    - **Username** currently logged in
    - **User role**
    - **Task ID / Assignment ID**, if applicable
    - **Date and time** when the issue occurred
    - **Exact error message**, if displayed
    - **Steps followed before the issue occurred**
    - **Screenshot** of the issue
    """
)


st.divider()


# ==========================================================
# COMMON ISSUES
# ==========================================================

st.subheader("🔧 Common Issues")


with st.expander("🔐 Login Problem"):

    st.write(
        """
        Check that the username and password are correct.

        If the problem continues, contact the **Data Analyst /
        designated system support person** and provide the username
        and screenshot of the issue.
        """
    )


with st.expander("📋 Task is Not Visible"):

    st.write(
        """
        Check whether the task has been assigned to the logged-in
        Coordinator.

        Verify the Coordinator ID and Task ID.

        If the task is still not visible, contact the **Data Analyst**
        with the Task ID / Assignment ID and screenshot.
        """
    )


with st.expander("📝 Daily Review Cannot Be Submitted"):

    st.write(
        """
        Check the following:

        1. The task is assigned to the logged-in Coordinator.
        2. The assignment is active.
        3. The review date is selected.
        4. The status is selected.
        5. Required progress / remarks are entered.

        If the issue continues, contact the **Data Analyst**.
        """ 
    )


with st.expander("👥 User Management Issue"):

    st.write(
        """
        User-management functions are role based.

        Developer and Admin users have administrative functions,
        while Coordinators have limited access.

        If you believe that your access or permissions are incorrect,
        contact the **Data Analyst / designated system support person**.
        """
    )


with st.expander("🔔 Notification Issue"):

    st.write(
        """
        Refresh the Notifications page first.

        Check whether the related task or Daily Review has been
        correctly recorded.

        If notifications are still not appearing correctly,
        contact the **Data Analyst**.
        """
    )


with st.expander("📊 Dashboard Data Not Updated"):

    st.write(
        """
        Refresh the page first.

        If the information is still not updated, verify that the
        related Task Assignment or Daily Review was successfully
        submitted.

        If the problem continues, contact the **Data Analyst** and
        provide the relevant Task ID / Assignment ID.
        """
    )


st.divider()


# ==========================================================
# REPORT AN ISSUE
# ==========================================================

st.subheader("✉️ Prepare a Support Request")

st.caption(
    "Complete the details below before contacting the Data Analyst."
)

with st.form("support_request_form"):

    issue_type = st.selectbox(
        "Issue Type",
        [
            "Login / Authentication",
            "User Management",
            "Task Management",
            "Daily Review",
            "Notifications",
            "Reports Dashboard",
            "System / Page Error",
            "Other"
        ]
    )

    issue_subject = st.text_input(
        "Issue Subject",
        placeholder="Example: Daily Review submission error"
    )

    issue_description = st.text_area(
        "Describe the Issue",
        height=150,
        placeholder=(
            "Describe what happened, what you expected, "
            "and any error message displayed."
        )
    )

    reference_id = st.text_input(
        "Task / Assignment / Review ID (if applicable)",
        placeholder="Example: TASK-001"
    )

    screenshot_available = st.radio(
        "Screenshot Available?",
        [
            "Yes",
            "No"
        ],
        horizontal=True
    )

    submitted = st.form_submit_button(
        "📨 Prepare Support Details",
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
                "Support details are ready to share with the Data Analyst."
            )

            st.markdown("### 📋 Support Summary")

            summary_data = {
                "Parameter": [
                    "Username",
                    "Role",
                    "Issue Type",
                    "Issue Subject",
                    "Reference ID",
                    "Screenshot Available"
                ],
                "Value": [
                    current_username,
                    current_role,
                    issue_type,
                    issue_subject.strip(),
                    reference_id.strip()
                    if reference_id.strip()
                    else "Not Applicable",
                    screenshot_available
                ]
            }

            st.dataframe(
                summary_data,
                use_container_width=True,
                hide_index=True
            )

            st.markdown("### 📝 Issue Description")

            st.info(
                issue_description.strip()
            )

            st.warning(
                """
                Please share the above information and any relevant
                screenshot with the **Data Analyst / designated system
                support person**.
                """
            )


st.divider()


# ==========================================================
# SUPPORT CHECKLIST
# ==========================================================

st.subheader("✅ Before Contacting the Data Analyst")

checklist = [
    "Refresh the page.",
    "Confirm that you are logged into the correct account.",
    "Check whether your role has permission for the requested action.",
    "Verify the Task ID / Assignment ID, if applicable.",
    "Check the Help Center.",
    "Check the System Manual.",
    "Record the exact error message.",
    "Take a screenshot of the problem."
]

for index, item in enumerate(checklist):

    st.checkbox(
        item,
        key=f"support_check_{index}"
    )


st.divider()


# ==========================================================
# SUPPORT FLOW
# ==========================================================

st.subheader("🔄 Support Flow")

support_flow = {
    "Step": [
        "1",
        "2",
        "3",
        "4"
    ],
    "Action": [
        "Refresh and re-check the page",
        "Check Help Center / System Manual",
        "Prepare issue details and screenshot",
        "Contact the Data Analyst"
    ]
}

st.dataframe(
    support_flow,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==========================================================
# SECURITY NOTICE
# ==========================================================

st.warning(
    """
    **🔐 Security Notice**

    Never share passwords, authentication secrets, API keys,
    confidential credentials, or other sensitive security
    information in a support request or screenshot.
    """
)


st.divider()


# ==========================================================
# FINAL SUPPORT MESSAGE
# ==========================================================

st.success(
    """
    🟢 For technical or portal-related issues, please contact the
    **Data Analyst / designated system support person** with the
    relevant issue details and screenshot.
    """
)


# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "Contact Support • Coordinator Monitoring & Task Management System"
)

st.caption(
    "Technical Support Contact: Data Analyst"
)
