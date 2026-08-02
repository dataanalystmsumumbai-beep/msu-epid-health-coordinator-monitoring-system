import streamlit as st

from core.navigation import require_login
from services.user_service import UserService

st.set_page_config(
    page_title="User Management",
    page_icon="👥",
    layout="wide"
)

require_login(["Developer", "Admin"])

st.title("👥 User Management")

st.divider()

users = UserService.get_all_users()

if users is None:
    users = []

stats = UserService.statistics()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Users",
        stats["total"]
    )

with c2:
    st.metric(
        "Developers",
        stats["developers"]
    )

with c3:
    st.metric(
        "Admins",
        stats["admins"]
    )

with c4:
    st.metric(
        "Coordinators",
        stats["coordinators"]
    )

st.divider()

tab1, tab2 = st.tabs(
    [
        "👥 User List",
        "🔍 Search"
    ]
)

with tab1:

    st.subheader("All Users")

    st.dataframe(
        users,
        use_container_width=True,
        hide_index=True
    )

with tab2:

    search = st.text_input(
        "Search User"
    )

    if search.strip():

        filtered = [

            u

            for u in users

            if search.lower() in str(u).lower()

        ]

    else:

        filtered = users

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

st.divider()

st.caption(
    "MSU / EPID Health Coordinator Monitoring System | User Management"
)
