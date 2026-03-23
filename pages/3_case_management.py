import streamlit as st
import pandas as pd
from utils.data_loader import load_data, save_data

st.title("📂 Case Management")

df = load_data()

if df.empty:
    st.info("No cases found.")
    st.stop()

st.sidebar.header("Filters")

status_filter = st.sidebar.multiselect(
    "Filter by Status",
    options=sorted([x for x in df["Status"].dropna().unique().tolist() if x != ""]),
    default=[]
)

province_filter = st.sidebar.multiselect(
    "Filter by Province",
    options=sorted([x for x in df["Province"].dropna().unique().tolist() if x != ""]),
    default=[]
)

category_filter = st.sidebar.multiselect(
    "Filter by Category",
    options=sorted([x for x in df["Category"].dropna().unique().tolist() if x != ""]),
    default=[]
)

search_text = st.sidebar.text_input("Search Caller Name / Case ID")

filtered_df = df.copy()

if status_filter:
    filtered_df = filtered_df[filtered_df["Status"].isin(status_filter)]

if province_filter:
    filtered_df = filtered_df[filtered_df["Province"].isin(province_filter)]

if category_filter:
    filtered_df = filtered_df[filtered_df["Category"].isin(category_filter)]

if search_text.strip():
    s = search_text.strip().lower()
    filtered_df = filtered_df[
        filtered_df["Caller Name"].astype(str).str.lower().str.contains(s, na=False) |
        filtered_df["Case ID"].astype(str).str.lower().str.contains(s, na=False)
    ]

st.subheader("Filtered Cases")
edited_df = st.data_editor(
    filtered_df,
    use_container_width=True,
    num_rows="dynamic",
    disabled=[
        "Case ID"
    ]
)

if st.button("Save Changes"):
    base_df = df.copy()

    for _, edited_row in edited_df.iterrows():
        case_id = edited_row["Case ID"]
        mask = base_df["Case ID"] == case_id
        for col in base_df.columns:
            if col in edited_row.index:
                base_df.loc[mask, col] = edited_row[col]

    save_data(base_df)
    st.success("Changes saved successfully.")

st.markdown("---")
st.subheader("All Cases")
st.dataframe(filtered_df, use_container_width=True)
