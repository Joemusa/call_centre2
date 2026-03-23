import streamlit as st
from google.oauth2.service_account import Credentials

def get_google_credentials():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    if "gcp_service_account" not in st.secrets:
        return None

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )
    return credentials
