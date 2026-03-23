import streamlit as st
from utils.data_loader import load_data

st.title("📊 Reports")

df = load_data()

if df.empty:
    st.info("No data available for reports.")
    st.stop()

st.subheader("Download Full Case Report")
csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV Report",
    data=csv_data,
    file_name="call_centre_report.csv",
    mime="text/csv"
)

st.subheader("Report Preview")
st.dataframe(df, use_container_width=True)
