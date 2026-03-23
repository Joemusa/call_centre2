import streamlit as st
from utils.data_loader import load_data
from utils.calculations import (
    calculate_metrics,
    category_summary,
    status_summary,
    province_summary,
    daily_trend,
)
from utils.charts import bar_chart, pie_chart, line_chart

st.title("🏠 Home Dashboard")

df = load_data()
metrics = calculate_metrics(df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Calls", metrics["total_calls"])
col2.metric("Open Cases", metrics["open_cases"])
col3.metric("Urgent Cases", metrics["urgent_cases"])
col4.metric("Resolved Cases", metrics["resolved_cases"])

st.markdown("---")

left, right = st.columns(2)

with left:
    st.subheader("Cases by Category")
    cat_df = category_summary(df)
    fig = bar_chart(cat_df, "Category", "Count", "Cases by Category")
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No category data available.")

with right:
    st.subheader("Cases by Status")
    stat_df = status_summary(df)
    fig = pie_chart(stat_df, "Status", "Count", "Cases by Status")
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No status data available.")

left2, right2 = st.columns(2)

with left2:
    st.subheader("Cases by Province")
    prov_df = province_summary(df)
    fig = bar_chart(prov_df, "Province", "Count", "Cases by Province")
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No province data available.")

with right2:
    st.subheader("Daily Call Trend")
    trend_df = daily_trend(df)
    fig = line_chart(trend_df, "Call Date", "Count", "Daily Call Trend")
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No trend data available.")

st.subheader("Recent Cases")
st.dataframe(df.tail(10), use_container_width=True)
