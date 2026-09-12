import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
from config.config import (
    ROLE_COORDINATOR,
    TASK_MASTER,
    COORDINATOR_TASK_MAP,
    DAILY_REVIEW
)
from utils.google_sheet import read_all
from core.navigation import logout_button
from services.task_assignment_service import TaskAssignmentService

st.set_page_config(page_title="Coordinator Dashboard", page_icon="👨‍⚕️", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

current_user = st.session_state.get("user", {})
current_role = str(current_user.get("Role", "")).strip()
current_user_id = str(current_user.get("Coordinator_ID", current_user.get("User_ID", ""))).strip()
current_username = str(current_user.get("Username", "")).strip()

if current_role != ROLE_COORDINATOR:
    st.error("Coordinator access required.")
    st.stop()

logout_button()

st.title("👨‍⚕️ Coordinator Dashboard")
st.caption(f"Welcome, {current_username}")
st.divider()


def safe_read(sheet_name):
    try:
        data = read_all(sheet_name)
        return data if data else []
    except Exception:
        return []


def parse_date(value):
    if value is None or str(value).strip() == "":
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = str(value).strip()
    for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y", "%d.%m.%Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    try:
        return pd.to_datetime(text, dayfirst=True).date()
    except Exception:
        return None


def normalize_status(value):
    return str(value or "").strip().lower()


tasks = safe_read(TASK_MASTER)
reviews = safe_read(DAILY_REVIEW)
try:
    assignments = TaskAssignmentService.get_all_assignments()
except Exception:
    assignments = []

my_assignments = [
    a for a in assignments
    if str(a.get("Coordinator_ID", "")).strip() == current_user_id
    and normalize_status(a.get("Status")) not in ["removed", "deleted", "inactive"]
]

task_lookup = {}
for task in tasks:
    task_id = str(task.get("Task_ID", "")).strip()
    if task_id:
        task_lookup[task_id] = task

# ----------------------------------------------------------
# TOP METRICS
# ----------------------------------------------------------
total_tasks = len(my_assignments)
completed_tasks = sum(normalize_status(a.get("Status")) == "completed" for a in my_assignments)
pending_tasks = sum(normalize_status(a.get("Status")) == "pending" for a in my_assignments)
in_progress_tasks = sum(normalize_status(a.get("Status")) in ["in progress", "in_progress"] for a in my_assignments)
completion_percentage = completed_tasks / total_tasks * 100 if total_tasks else 0

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("📋 Assigned", total_tasks)
with c2:
    st.metric("✅ Completed", completed_tasks)
with c3:
    st.metric("⏳ Pending", pending_tasks)
with c4:
    st.metric("🔄 In Progress", in_progress_tasks)
with c5:
    st.metric("📈 Completion", f"{completion_percentage:.0f}%")

st.divider()

st.subheader("📊 Overall Task Progress")
st.progress(completion_percentage / 100)
st.caption(f"{completion_percentage:.1f}% of assigned tasks completed")
st.divider()

# ----------------------------------------------------------
# DAILY REVIEW MONITORING
# ----------------------------------------------------------
st.subheader("📅 Daily Review Monitoring")
st.caption("Daily tasks are expected from the assignment date through today. A missing submission is shown as Missing / Not Reporting.")

# Build review lookup using the confirmed Daily Review headers.
review_lookup = set()
for review in reviews:
    coordinator_id = str(review.get("Coordinator_ID", "")).strip()
    task_id = str(review.get("Task_ID", "")).strip()
    review_date = parse_date(review.get("Date"))
    if coordinator_id and task_id and review_date:
        review_lookup.add((coordinator_id, task_id, review_date))

expected_rows = []
today = date.today()

for assignment in my_assignments:
    task_id = str(assignment.get("Task_ID", "")).strip()
    task = task_lookup.get(task_id, {})
    frequency = str(task.get("Frequency", assignment.get("Frequency", ""))).strip()
    task_name = str(task.get("Task_Name", task.get("Task", task_id))).strip()
    task_status = normalize_status(task.get("Status"))

    if frequency.lower() != "daily":
        continue
    if task_status != "active":
        continue

    assigned_date = parse_date(assignment.get("Assigned_Date")) or today
    due_date = parse_date(assignment.get("Due_Date"))
    end_date = today
    if due_date and due_date < end_date:
        end_date = due_date
    if assigned_date > end_date:
        continue

    current_date = assigned_date
    while current_date <= end_date:
        submitted = (current_user_id, task_id, current_date) in review_lookup
        expected_rows.append({
            "Date": current_date,
            "Task": task_name,
            "Task_ID": task_id,
            "Assignment_ID": assignment.get("Assignment_ID", ""),
            "Status": "Submitted" if submitted else "Missing / Not Reporting",
            "Review": "Yes" if submitted else "No"
        })
        current_date += timedelta(days=1)

if expected_rows:
    expected_df = pd.DataFrame(expected_rows)
    expected_df["Date"] = pd.to_datetime(expected_df["Date"])

    min_expected = expected_df["Date"].min().date()
    max_expected = expected_df["Date"].max().date()

    f1, f2 = st.columns(2)
    with f1:
        start_date = st.date_input("From Date", value=min_expected, min_value=min_expected, max_value=max_expected, key="dashboard_from_date_v3")
    with f2:
        end_date = st.date_input("To Date", value=max_expected, min_value=min_expected, max_value=max_expected, key="dashboard_to_date_v3")

    if start_date > end_date:
        st.warning("From Date cannot be later than To Date.")
    else:
        filtered = expected_df[
            (expected_df["Date"].dt.date >= start_date)
            & (expected_df["Date"].dt.date <= end_date)
        ].copy()

        expected_count = len(filtered)
        submitted_count = int((filtered["Status"] == "Submitted").sum())
        missing_count = int((filtered["Status"] == "Missing / Not Reporting").sum())
        review_completion = submitted_count / expected_count * 100 if expected_count else 0

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Expected", expected_count)
        with m2:
            st.metric("Submitted", submitted_count)
        with m3:
            st.metric("Missing", missing_count)
        with m4:
            st.metric("Review Completion", f"{review_completion:.1f}%")

        st.progress(review_completion / 100)

        display_df = filtered[["Date", "Task", "Assignment_ID", "Status"]].copy()
        display_df["Date"] = display_df["Date"].dt.strftime("%d-%m-%Y")
        st.dataframe(display_df, use_container_width=True, hide_index=True)

else:
    st.info("No active Daily task is currently assigned to you.")

st.divider()

# ----------------------------------------------------------
# ASSIGNED TASKS
# ----------------------------------------------------------
st.subheader("📋 My Assigned Tasks")

if not my_assignments:
    st.info("No tasks have been assigned to you.")
else:
    task_rows = []
    for assignment in my_assignments:
        task_id = str(assignment.get("Task_ID", "")).strip()
        task = task_lookup.get(task_id, {})
        task_rows.append({
            "Assignment ID": assignment.get("Assignment_ID", ""),
            "Task": str(task.get("Task_Name", task.get("Task", task_id))).strip(),
            "Assigned Date": assignment.get("Assigned_Date", ""),
            "Due Date": assignment.get("Due_Date", ""),
            "Priority": assignment.get("Priority", ""),
            "Status": assignment.get("Status", "Pending"),
            "Remarks": assignment.get("Remarks", "")
        })
    st.dataframe(pd.DataFrame(task_rows), use_container_width=True, hide_index=True)

st.divider()

# ----------------------------------------------------------
# REVIEW HISTORY
# ----------------------------------------------------------
st.subheader("📚 My Review History")

my_reviews = [
    review for review in reviews
    if str(review.get("Coordinator_ID", "")).strip() == current_user_id
    or str(review.get("Username", "")).strip() == current_username
]

if my_reviews:
    st.dataframe(pd.DataFrame(my_reviews), use_container_width=True, hide_index=True)
else:
    st.info("No Daily Reviews submitted yet.")

st.divider()

# ----------------------------------------------------------
# NAVIGATION
# ----------------------------------------------------------
st.subheader("⚡ Quick Actions")
q1, q2 = st.columns(2)
with q1:
    if st.button("📋 Task Management", use_container_width=True):
        st.switch_page("pages/04_Task_Management.py")
with q2:
    if st.button("📝 Daily Review", use_container_width=True):
        st.switch_page("pages/03_Daily_Review.py")
