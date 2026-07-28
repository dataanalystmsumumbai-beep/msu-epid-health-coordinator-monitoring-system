import streamlit as st
from google.oauth2.service_account import Credentials

# -------------------------------
# Google Sheet Configuration
# -------------------------------

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
