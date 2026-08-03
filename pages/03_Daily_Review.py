import streamlit as st
from datetime import date

from core.navigation import require_login
from core.session import logout

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Daily Review",
    page_icon="📝",
    layout="wide"
)

require_login("Coordinator")

# =====================================================
# Sidebar
# =====================================================

with st.sidebar:

    st.title("📝 Daily Review")

    st.write(f"**User :** {st.session_state.get('full_name','')}")

    st.write(f"**Role :** {st.session_state.get('role','')}")

    st.divider()

    if st.button(
    "🚪 Logout",
    use_container_width=True
):
    logout()
    st.stop()

# =====================================================
# Header
# =====================================================

st.title("📝 Daily Review")

st.caption("Daily Review Submission")

st.divider()

# =====================================================
# Review Form
# =====================================================

with st.form("daily_review_form"):

    review_date = st.date_input(
        "Review Date",
        value=date.today()
    )

    task = st.text_input(
        "Task Name"
    )

    status = st.selectbox(

        "Status",

        [
            "Completed",
            "Pending",
            "In Progress"
        ]

    )

    remarks = st.text_area(
        "Remarks"
    )

    submitted = st.form_submit_button(
        "✅ Submit Review",
        use_container_width=True
    )

if submitted:

    st.success("Daily Review Submitted Successfully.")

st.divider()

# =====================================================
# Today's Summary
# =====================================================

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Completed",
        "0"
    )

with c2:

    st.metric(
        "Pending",
        "0"
    )

with c3:

    st.metric(
        "In Progress",
        "0"
    )

st.divider()

st.info(
    "Submitted reviews will appear here after Google Sheet integration."
)
