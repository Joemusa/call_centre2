# app.py
import streamlit as st

st.set_page_config(page_title="Church Community Call Centre", layout="wide")

st.title("📞 Church Community Call Centre Dashboard")
st.markdown("Welcome to the main dashboard. Use the sidebar to navigate through the system.")

st.info("This is the starter app. Add pages in the pages folder for full functionality.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Calls", 0)
col2.metric("Open Cases", 0)
col3.metric("Urgent Cases", 0)
col4.metric("Resolved Cases", 0)

st.subheader("System Overview")
st.write("Use this dashboard to monitor calls, track cases, and review agent performance.")

# requirements.txt
# streamlit
# pandas
# plotly
# gspread
# google-auth

# pages/1_Home.py
import streamlit as st
import pandas as pd

st.title("🏠 Home Dashboard")
st.write("Summary of call centre activity")

# pages/2_New_Case.py
import streamlit as st

st.title("📝 New Case Capture")
with st.form("new_case_form"):
    caller_name = st.text_input("Caller Name")
    contact = st.text_input("Contact Number")
    category = st.selectbox("Category", ["Counselling", "Prayer", "Food Support", "Family Issues", "Other"])
    urgency = st.selectbox("Urgency", ["Low", "Medium", "High", "Critical"])
    description = st.text_area("Description of Problem")
    submitted = st.form_submit_button("Save Case")

    if submitted:
        st.success("Case saved successfully")

# pages/3_Case_Management.py
import streamlit as st
import pandas as pd

st.title("📂 Case Management")
st.write("View and manage all open and resolved cases")

data = pd.DataFrame(columns=[
    "Case ID", "Date", "Caller Name", "Category", "Urgency", "Assigned Agent", "Status"
])
st.dataframe(data, use_container_width=True)

# pages/4_Agent_Performance.py
import streamlit as st

st.title("👤 Agent Performance")
st.write("Track calls handled, case closures, and service performance")

# pages/5_Reports.py
import streamlit as st

st.title("📊 Reports")
st.write("Generate daily, weekly, and monthly reports")

# utils/data_loader.py
import pandas as pd

def load_data():
    return pd.DataFrame()

# utils/calculations.py
def calculate_metrics(df):
    return {
        "total_calls": len(df),
        "open_cases": 0,
        "urgent_cases": 0,
        "resolved_cases": 0,
    }

# utils/charts.py
# Add chart helper functions here

