import streamlit as st

from core.navigation import require_login

st.set_page_config(
    page_title="Help Center",
    page_icon="❓",
    layout="wide"
)

require_login([
    "Developer",
    "Admin",
    "Coordinator"
])

st.title("❓ Help Center")

st.divider()

tab1, tab2, tab3 = st.tabs([
    "📖 User Guide",
    "☎ Contact",
    "ℹ About"
])

# =====================================================
# User Guide
# =====================================================

with tab1:

    st.subheader("System Modules")

    st.info("""
**Developer**
- User Management
- Task Management
- System Settings

**Admin**
- Manage Coordinators
- Daily Review Monitoring
- Reports

**Coordinator**
- Daily Review
- Task Submission
- Progress Tracking
""")

# =====================================================
# Contact
# =====================================================

with tab2:

    st.subheader("Support")

    st.write("📧 Email : support@msu.in")

    st.write("📞 Phone : +91-9999999999")

    st.write("🌐 Website : https://msu.in")

# =====================================================
# About
# =====================================================

with tab3:

    st.subheader("About System")

    st.success("""
MSU / EPID Health Coordinator Monitoring System

Version : 1.0

Developed for:
Health Coordinator Monitoring,
Daily Review,
Task Assignment,
Performance Tracking.
""")

st.divider()

st.caption(
    "© 2026 MSU / EPID Health Coordinator Monitoring System"
)
