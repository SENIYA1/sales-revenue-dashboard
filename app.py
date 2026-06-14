import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales & Revenue Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales & Revenue Analysis Dashboard")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
else:
    df = pd.read_csv("sales.csv")

df["Date"] = pd.to_datetime(df["Date"])

st.sidebar.header("🔍 Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    df["Date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Date"].max()
)

category = st.sidebar.selectbox(
    "Category",
    ["All"] + list(df["Category"].unique())
)

product = st.sidebar.selectbox(
    "Product",
    ["All"] + list(df["Product"].unique())
)

filtered_df = df.copy()

filtered_df = filtered_df[
    (filtered_df["Date"] >= pd.to_datetime(start_date))
    & (filtered_df["Date"] <= pd.to_datetime(end_date))
]

if category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == category
    ]

if product != "All":
    filtered_df = filtered_df[
        filtered_df["Product"] == product
    ]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

total_sales = filtered_df["Sales"].sum()
total_revenue = filtered_df["Revenue"].sum()
total_orders = len(filtered_df)

monthly_growth_data = (
    filtered_df.groupby(
        filtered_df["Date"].dt.to_period("M")
    )["Revenue"]
    .sum()
)

growth = 0

if len(monthly_growth_data) >= 2:
    previous = monthly_growth_data.iloc[-2]
    current = monthly_growth_data.iloc[-1]

    if previous != 0:
        growth = ((current - previous) / previous) * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sales",
        f"₹{total_sales:,}"
    )

with col2:
    st.metric(
        "Total Revenue",
        f"₹{total_revenue:,}"
    )

with col3:
    st.metric(
        "Total Orders",
        total_orders
    )

with col4:
    st.metric(
        "Revenue Growth",
        f"{growth:.2f}%"
    )

st.markdown("---")

monthly_revenue = (
    filtered_df.groupby("Date")["Revenue"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    monthly_revenue,
    x="Date",
    y="Revenue",
    title="📈 Revenue Trend",
    markers=True
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

col5, col6 = st.columns(2)

with col5:
    top_products = (
        filtered_df.groupby("Product")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(
            by="Revenue",
            ascending=False
        )
    )

    fig2 = px.bar(
        top_products,
        x="Product",
        y="Revenue",
        title="🏆 Top Performing Products"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

with col6:
    category_revenue = (
        filtered_df.groupby("Category")["Revenue"]
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        category_revenue,
        names="Category",
        values="Revenue",
        title="🥧 Revenue by Category"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

st.markdown("---")

monthly_comparison = (
    filtered_df.groupby(
        filtered_df["Date"].dt.month_name()
    )["Revenue"]
    .sum()
    .reset_index()
)

fig4 = px.bar(
    monthly_comparison,
    x="Date",
    y="Revenue",
    title="📊 Monthly Revenue Comparison"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.markdown("---")

st.subheader("🏆 Top 5 Products")

top5 = (
    filtered_df.groupby("Product")["Revenue"]
    .sum()
    .reset_index()
    .sort_values(
        by="Revenue",
        ascending=False
    )
    .head(5)
)

st.dataframe(
    top5,
    use_container_width=True
)

st.markdown("---")

st.subheader("📌 Business Insights")

best_product = (
    filtered_df.groupby("Product")["Revenue"]
    .sum()
    .idxmax()
)

best_month = (
    filtered_df.groupby(
        filtered_df["Date"].dt.month_name()
    )["Revenue"]
    .sum()
    .idxmax()
)

col7, col8 = st.columns(2)

with col7:
    st.success(
        f"🏆 Best Product: {best_product}"
    )

with col8:
    st.info(
        f"📅 Best Month: {best_month}"
    )

st.markdown("---")

st.subheader("📋 Sales Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)

csv = filtered_df.to_csv(
    index=False
)

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="filtered_sales.csv",
    mime="text/csv"
)