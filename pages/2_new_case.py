import streamlit as st
from datetime import datetime, date
from utils.data_loader import load_data, append_case

st.title("📝 New Case Capture")

existing_df = load_data()

def generate_case_id(df):
    if df.empty:
        return "CC-1001"

    ids = df["Case ID"].astype(str).tolist()
    numbers = []

    for item in ids:
        try:
            numbers.append(int(item.split("-")[1]))
        except Exception:
            continue

    if not numbers:
        return "CC-1001"

    return f"CC-{max(numbers) + 1}"


with st.form("new_case_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        caller_name = st.text_input("Caller Name")
        contact = st.text_input("Contact Number")
        gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
        province = st.text_input("Province", value="Gauteng")
        branch = st.text_input("Branch")
        category = st.selectbox(
            "Category",
            ["Prayer", "Counselling", "Food Support", "Family Issues", "Health", "Other"]
        )
        subcategory = st.text_input("Subcategory")

    with col2:
        urgency = st.selectbox("Urgency Level", ["Low", "Medium", "High", "Critical"])
        assigned_agent = st.text_input("Assigned Agent")
        status = st.selectbox("Status", ["Open", "In Progress", "Pending", "Resolved"])
        follow_up_date = st.date_input("Follow-up Date", value=date.today())
        call_date = st.date_input("Call Date", value=date.today())
        call_time = st.time_input("Call Time", value=datetime.now().time())

    description = st.text_area("Description of Problem")
    resolution_notes = st.text_area("Resolution Notes")

    submitted = st.form_submit_button("Save Case")

    if submitted:
        if not caller_name.strip():
            st.error("Caller Name is required.")
        elif not contact.strip():
            st.error("Contact Number is required.")
        elif not description.strip():
            st.error("Description is required.")
        else:
            case_id = generate_case_id(existing_df)

            case_data = {
                "Case ID": case_id,
                "Date": str(call_date),
                "Time": call_time.strftime("%H:%M"),
                "Caller Name": caller_name.strip(),
                "Contact Number": contact.strip(),
                "Gender": gender,
                "Province": province.strip(),
                "Branch": branch.strip(),
                "Category": category,
                "Subcategory": subcategory.strip(),
                "Description": description.strip(),
                "Urgency Level": urgency,
                "Assigned Agent": assigned_agent.strip(),
                "Status": status,
                "Follow-up Date": str(follow_up_date),
                "Resolution Notes": resolution_notes.strip(),
            }

            append_case(case_data)
            st.success(f"Case {case_id} saved successfully.")
