import pandas as pd


def safe_upper_series(df: pd.DataFrame, column: str):
    if column not in df.columns:
        return pd.Series(dtype="object")
    return df[column].fillna("").astype(str).str.strip().str.upper()


def calculate_metrics(df: pd.DataFrame):
    total_calls = len(df)

    status_upper = safe_upper_series(df, "Status")
    urgency_upper = safe_upper_series(df, "Urgency Level")

    open_cases = status_upper.isin(["OPEN", "IN PROGRESS", "PENDING"]).sum()
    urgent_cases = urgency_upper.isin(["HIGH", "CRITICAL"]).sum()
    resolved_cases = status_upper.eq("RESOLVED").sum()

    return {
        "total_calls": int(total_calls),
        "open_cases": int(open_cases),
        "urgent_cases": int(urgent_cases),
        "resolved_cases": int(resolved_cases),
    }


def category_summary(df: pd.DataFrame):
    if df.empty:
        return pd.DataFrame(columns=["Category", "Count"])

    result = (
        df.groupby("Category", dropna=False)
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )
    return result


def status_summary(df: pd.DataFrame):
    if df.empty:
        return pd.DataFrame(columns=["Status", "Count"])

    result = (
        df.groupby("Status", dropna=False)
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )
    return result


def agent_summary(df: pd.DataFrame):
    if df.empty:
        return pd.DataFrame(columns=["Assigned Agent", "Cases Handled"])

    result = (
        df.groupby("Assigned Agent", dropna=False)
        .size()
        .reset_index(name="Cases Handled")
        .sort_values("Cases Handled", ascending=False)
    )
    return result


def province_summary(df: pd.DataFrame):
    if df.empty:
        return pd.DataFrame(columns=["Province", "Count"])

    result = (
        df.groupby("Province", dropna=False)
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )
    return result


def daily_trend(df: pd.DataFrame):
    if df.empty:
        return pd.DataFrame(columns=["Date", "Count"])

    temp = df.copy()
    temp["Date"] = pd.to_datetime(temp["Date"], errors="coerce")
    temp = temp.dropna(subset=["Date"])

    result = (
        temp.groupby(temp["Date"].dt.date)
        .size()
        .reset_index(name="Count")
        .rename(columns={"Date": "Call Date"})
    )
    return result
