import streamlit as st
from utils.data_loader import load_data
from utils.calculations import agent_summary
from utils.charts import bar_chart

st.title("👤 Agent Performance")

df = load_data()

if df.empty:
    st.info("No cases available.")
    st.stop()

summary_df = agent_summary(df)

st.subheader("Cases Handled by Agent")
st.dataframe(summary_df, use_container_width=True)

fig = bar_chart(summary_df, "Assigned Agent", "Cases Handled", "Agent Performance")
if fig:
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No agent performance data available.")
