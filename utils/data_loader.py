import os
import pandas as pd
import gspread
import streamlit as st
from utils.auth import get_google_credentials

EXPECTED_COLUMNS = [
    "Case ID",
    "Date",
    "Time",
    "Caller Name",
    "Contact Number",
    "Gender",
    "Province",
    "Branch",
    "Category",
    "Subcategory",
    "Description",
    "Urgency Level",
    "Assigned Agent",
    "Status",
    "Follow-up Date",
    "Resolution Notes",
]

LOCAL_FILE = "data/cases.csv"


def empty_dataframe():
    return pd.DataFrame(columns=EXPECTED_COLUMNS)


def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return empty_dataframe()

    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    return df[EXPECTED_COLUMNS]


def load_local_data():
    if not os.path.exists(LOCAL_FILE):
        df = empty_dataframe()
        os.makedirs("data", exist_ok=True)
        df.to_csv(LOCAL_FILE, index=False)
        return df

    df = pd.read_csv(LOCAL_FILE, dtype=str).fillna("")
    return ensure_columns(df)


def save_local_data(df: pd.DataFrame):
    os.makedirs("data", exist_ok=True)
    df = ensure_columns(df)
    df.to_csv(LOCAL_FILE, index=False)


def get_gsheet():
    credentials = get_google_credentials()
    if credentials is None:
        return None

    if "GOOGLE_SHEET_NAME" not in st.secrets or "GOOGLE_WORKSHEET_NAME" not in st.secrets:
        return None

    client = gspread.authorize(credentials)
    sheet = client.open(st.secrets["GOOGLE_SHEET_NAME"]).worksheet(
        st.secrets["GOOGLE_WORKSHEET_NAME"]
    )
    return sheet


def load_data():
    try:
        sheet = get_gsheet()
        if sheet is not None:
            records = sheet.get_all_records()
            df = pd.DataFrame(records)
            return ensure_columns(df)
    except Exception:
        pass

    return load_local_data()


def overwrite_google_sheet(df: pd.DataFrame):
    sheet = get_gsheet()
    if sheet is None:
        return False

    df = ensure_columns(df)
    values = [df.columns.tolist()] + df.astype(str).values.tolist()
    sheet.clear()
    sheet.update(values)
    return True


def save_data(df: pd.DataFrame):
    saved_to_google = False

    try:
        saved_to_google = overwrite_google_sheet(df)
    except Exception:
        saved_to_google = False

    save_local_data(df)
    return saved_to_google


def append_case(case_data: dict):
    df = load_data()
    new_row = pd.DataFrame([case_data])
    df = pd.concat([df, new_row], ignore_index=True)
    df = ensure_columns(df)
    save_data(df)
    return df
