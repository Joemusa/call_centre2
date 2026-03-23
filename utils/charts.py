import plotly.express as px


def bar_chart(df, x, y, title):
    if df.empty:
        return None
    return px.bar(df, x=x, y=y, title=title)


def pie_chart(df, names, values, title):
    if df.empty:
        return None
    return px.pie(df, names=names, values=values, title=title)


def line_chart(df, x, y, title):
    if df.empty:
        return None
    return px.line(df, x=x, y=y, title=title, markers=True)
