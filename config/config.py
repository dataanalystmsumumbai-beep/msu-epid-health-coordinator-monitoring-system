import streamlit as st
from google.oauth2.service_account import Credentials

# ------------------------------
# Google Sheet Configuration
# ------------------------------

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_NAME = "MSU HCMS Database"


def get_google_credentials():
    return Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )


# ------------------------------
# Application Configuration
# ------------------------------

APP_NAME = "MSU EPID Health Coordinator Monitoring System"

APP_VERSION = "3.0.0"

DEVELOPER_USERNAME = "developer"

MAX_COORDINATOR_EDIT = 6

PASSWORD_MIN_LENGTH = 8

PASSWORD_MAX_LENGTH = 10

ALLOWED_SPECIAL_CHARACTERS = "@#$-._"
