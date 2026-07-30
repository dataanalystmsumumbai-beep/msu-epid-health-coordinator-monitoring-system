import streamlit as st
from google.oauth2.service_account import Credentials

# ======================================================
# Google Credentials
# ======================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_NAME = "MSU-EPID Health Coordinator Monitoring System Database"


def get_google_credentials():
    return Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )


# ======================================================
# Google Sheet Names
# ======================================================

USER_MASTER = "01_User_Master"

COORDINATOR_MASTER = "02_Coordinator_Master"

TASK_MASTER = "03_Task_Master"

COORDINATOR_TASK_MAP = "04_Coordinator_Task_Map"

DAILY_REVIEW = "05_Daily_Review"

LOGIN_HISTORY = "06_Login_History"

AUDIT_LOG = "07_Audit_Log"

SYSTEM_SETTINGS = "08_System_Settings"

APP_MANUAL = "09_App_Manual"

NOTIFICATIONS = "10_Notifications"


# ======================================================
# Application
# ======================================================

APP_NAME = "MSU EPID Health Coordinator Monitoring System"

APP_VERSION = "3.0.0"

APP_OWNER = "MSU / EPID"

APP_ENVIRONMENT = "Production"


# ======================================================
# Security
# ======================================================

PASSWORD_MIN_LENGTH = 8

PASSWORD_MAX_LENGTH = 20

MAX_LOGIN_ATTEMPTS = 5

SESSION_TIMEOUT_MINUTES = 30

ALLOWED_SPECIAL_CHARACTERS = "@#$-._"


# ======================================================
# Roles
# ======================================================

ROLE_DEVELOPER = "Developer"

ROLE_ADMIN = "Admin"

ROLE_COORDINATOR = "Coordinator"

ROLES = [
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR
]


# ======================================================
# Coordinator
# ======================================================

MAX_COORDINATOR_EDIT = 6


# ======================================================
# Status
# ======================================================

STATUS_ACTIVE = "ACTIVE"

STATUS_INACTIVE = "INACTIVE"

STATUS_PENDING = "PENDING"

STATUS_COMPLETED = "COMPLETED"


# ======================================================
# Date Formats
# ======================================================

DATE_FORMAT = "%d-%m-%Y"

DATETIME_FORMAT = "%d-%m-%Y %H:%M"

TIME_FORMAT = "%H:%M"


# ======================================================
# Dashboard Refresh
# ======================================================

AUTO_REFRESH_SECONDS = 300
