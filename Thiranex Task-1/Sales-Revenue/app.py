import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="NOVA | Sales Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# PREMIUM CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #F5F7FB;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10172A 0%, #18233D 100%);
}

[data-testid="stSidebar"] * {
    color: #E8EDF8;
}

[data-testid="stSidebar"] .stRadio label {
    color: #E8EDF8;
}

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #10172A;
    margin-bottom: 0px;
}

.subtitle {
    color: #75809A;
    font-size: 14px;
    margin-top: 5px;
    margin-bottom: 24px;
}

.section-title {
    font-size: 21px;
    font-weight: 700;
    color: #10172A;
    margin-top: 18px;
    margin-bottom: 12px;
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #E8ECF4;
    box-shadow: 0 5px 20px rgba(25, 40, 75, 0.04);
    min-height: 135px;
}

.metric-label {
    font-size: 13px;
    color: #7B8499;
    font-weight: 600;
}

.metric-value {
    font-size: 28px;
    font-weight: 800;
    color: #10172A;
    margin-top: 10px;
}

.metric-note {
    font-size: 12px;
    color: #16A085;
    margin-top: 8px;
}

div[data-testid="stPlotlyChart"] {
    background: white;
    border-radius: 16px;
    padding: 10px;
    border: 1px solid #E8ECF4;
}

div[data-testid="stDataFrame"] {
    background: white;
    border-radius: 14px;
}

.stButton button {
    border-radius: 10px;
    font-weight: 600;
}

hr {
    border-color: #29334B;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="padding:12px 0 22px 0;">
        <div style="font-size:12px;color:#A5B4D4;letter-spacing:3px;">
            SALES INTELLIGENCE
        </div>
        <div style="font-size:28px;font-weight:800;color:white;margin-top:8px;">
            NOVA<span style="color:#7C9CFF;">.</span>
        </div>
        <div style="font-size:12px;color:#A5B4D4;margin-top:4px;">
            Revenue Analytics Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Navigation")

    page = st.radio(
        "Navigate",
        ["Overview", "Product Analysis", "Regional Analysis", "Sales Data"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### Data Source")

    uploaded_file = st.file_uploader(
        "Upload sales CSV or Excel",
        type=["csv", "xlsx"]
    )

    st.caption("Upload your own dataset or use the included sample data.")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_sample_data():
    file_path = Path(__file__).parent / "sales_data.csv"

    if file_path.exists():
        return pd.read_csv(file_path)

    return pd.DataFrame({
        "Order_ID": ["ORD001", "ORD002"],
        "Date": ["2026-01-05", "2026-01-12"],
        "Product": ["Laptop", "Headphones"],
        "Category": ["Electronics", "Accessories"],
        "Region": ["South", "North"],
        "Quantity": [2, 5],
        "Unit_Price": [55000, 2000]
    })

try:
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
    else:
        df = load_sample_data()

    # Normalize column names
    df.columns = df.columns.str.strip()

    required_columns = [
        "Order_ID", "Date", "Product", "Category",
        "Region", "Quantity", "Unit_Price"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        st.error(
            "Missing required columns: "
            + ", ".join(missing)
        )
        st.info(
            "Required columns: Order_ID, Date, Product, "
            "Category, Region, Quantity, Unit_Price"
        )
        st.stop()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")

    df = df.dropna(
        subset=["Date", "Quantity", "Unit_Price",
                "Product", "Category", "Region"]
    )

    df["Revenue"] = df["Quantity"] * df["Unit_Price"]
    df["Month"] = df["Date"].dt.strftime("%b %Y")

    if df.empty:
        st.error("No valid sales records found in the uploaded file.")
        st.stop()

except Exception as e:
    st.error(f"Could not load the dataset: {e}")
    st.stop()

# --------------------------------------------------
# FILTERS
# --------------------------------------------------
with st.sidebar:
    st.markdown("### Filters")

    regions = sorted(df["Region"].dropna().unique())
    selected_regions = st.multiselect(
        "Region",
        regions,
        default=regions
    )

    products = sorted(df["Product"].dropna().unique())
    selected_products = st.multiselect(
        "Product",
        products,
        default=products
    )

    categories = sorted(df["Category"].dropna().unique())
    selected_categories = st.multiselect(
        "Category",
        categories,
        default=categories
    )

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

# Apply filters
filtered_df = df[
    df["Region"].isin(selected_regions)
    & df["Product"].isin(selected_products)
    & df["Category"].isin(selected_categories)
].copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= start_date)
        & (filtered_df["Date"].dt.date <= end_date)
    ]

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def money(value):
    return f"₹{value:,.0f}"

def metric_card(label, value, note):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)

def chart_layout(fig, height=350):
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=45, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter", color="#75809A"),
        title_font=dict(size=16, color="#10172A"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EDF0F6",
        zeroline=False
    )
    return fig

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------
st.markdown(
    '<div class="main-title">Sales Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Monitor revenue, discover product trends, and explore '
    'your business performance in real time.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"**Selected view:** {page} &nbsp;&nbsp; "
    f"**Records:** {len(filtered_df):,}",
    unsafe_allow_html=True
)

if filtered_df.empty:
    st.warning("No records match the selected filters. Adjust your filters.")
    st.stop()

# --------------------------------------------------
# METRICS
# --------------------------------------------------
total_revenue = filtered_df["Revenue"].sum()
total_orders = filtered_df["Order_ID"].nunique()
units_sold = filtered_df["Quantity"].sum()
average_order = (
    total_revenue / total_orders if total_orders else 0
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    metric_card(
        "TOTAL REVENUE",
        money(total_revenue),
        "Revenue from filtered sales"
    )

with m2:
    metric_card(
        "TOTAL ORDERS",
        f"{total_orders:,}",
        "Unique order count"
    )

with m3:
    metric_card(
        "UNITS SOLD",
        f"{units_sold:,.0f}",
        "Total quantity sold"
    )

with m4:
    metric_card(
        "AVG. ORDER VALUE",
        money(average_order),
        "Revenue per unique order"
    )

# --------------------------------------------------
# OVERVIEW PAGE
# --------------------------------------------------
if page == "Overview":

    st.markdown(
        '<div class="section-title">Revenue Performance</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1.65, 1])

    with left:
        monthly = (
            filtered_df
            .groupby(filtered_df["Date"].dt.to_period("M"))["Revenue"]
            .sum()
            .reset_index()
        )
        monthly["Month"] = monthly["Date"].dt.strftime("%b %Y")

        fig = px.area(
            monthly,
            x="Month",
            y="Revenue",
            markers=True,
            title="Monthly Revenue Trend",
            color_discrete_sequence=["#6179E8"]
        )
        fig.update_traces(
            line=dict(width=3),
            fillcolor="rgba(97,121,232,0.15)"
        )
        fig.update_yaxes(title="Revenue (₹)")
        st.plotly_chart(
            chart_layout(fig),
            use_container_width=True
        )

    with right:
        category_sales = (
            filtered_df.groupby("Category")["Revenue"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            category_sales,
            names="Category",
            values="Revenue",
            hole=0.65,
            title="Revenue by Category",
            color_discrete_sequence=[
                "#6179E8", "#20BFA9", "#F5A623", "#E56B8A"
            ]
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent"
        )
        st.plotly_chart(
            chart_layout(fig),
            use_container_width=True
        )

    st.markdown(
        '<div class="section-title">Top Performing Products</div>',
        unsafe_allow_html=True
    )

    top_products = (
        filtered_df.groupby("Product")["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Revenue", ascending=True)
    )

    fig = px.bar(
        top_products,
        x="Revenue",
        y="Product",
        orientation="h",
        title="Revenue by Product",
        text_auto=",.0f",
        color="Revenue",
        color_continuous_scale=["#A5B4FC", "#4F46E5"]
    )
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(title="Revenue (₹)")
    fig.update_yaxes(title="")
    st.plotly_chart(
        chart_layout(fig, 400),
        use_container_width=True
    )

# --------------------------------------------------
# PRODUCT ANALYSIS
# --------------------------------------------------
elif page == "Product Analysis":

    st.markdown(
        '<div class="section-title">Product Performance</div>',
        unsafe_allow_html=True
    )

    product_summary = (
        filtered_df.groupby(["Product", "Category"])
        .agg(
            Units_Sold=("Quantity", "sum"),
            Revenue=("Revenue", "sum"),
            Orders=("Order_ID", "nunique")
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    left, right = st.columns(2)

    with left:
        fig = px.bar(
            product_summary.sort_values("Revenue"),
            x="Revenue",
            y="Product",
            orientation="h",
            title="Revenue by Product",
            color="Revenue",
            color_continuous_scale=["#A5B4FC", "#4F46E5"]
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(
            chart_layout(fig),
            use_container_width=True
        )

    with right:
        fig = px.bar(
            product_summary.sort_values("Units_Sold"),
            x="Units_Sold",
            y="Product",
            orientation="h",
            title="Units Sold by Product",
            color="Units_Sold",
            color_continuous_scale=["#99F6E4", "#0D9488"]
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(
            chart_layout(fig),
            use_container_width=True
        )

    st.markdown("### Product Summary")
    st.dataframe(
        product_summary,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Revenue": st.column_config.NumberColumn(
                "Revenue (₹)", format="₹%.2f"
            )
        }
    )

# --------------------------------------------------
# REGIONAL ANALYSIS
# --------------------------------------------------
elif page == "Regional Analysis":

    st.markdown(
        '<div class="section-title">Regional Performance</div>',
        unsafe_allow_html=True
    )

    regional = (
        filtered_df.groupby("Region")
        .agg(
            Revenue=("Revenue", "sum"),
            Units_Sold=("Quantity", "sum"),
            Orders=("Order_ID", "nunique")
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    left, right = st.columns(2)

    with left:
        fig = px.bar(
            regional.sort_values("Revenue"),
            x="Revenue",
            y="Region",
            orientation="h",
            title="Revenue by Region",
            color="Revenue",
            color_continuous_scale=["#C4B5FD", "#7C3AED"]
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(
            chart_layout(fig),
            use_container_width=True
        )

    with right:
        fig = px.pie(
            regional,
            names="Region",
            values="Revenue",
            hole=0.55,
            title="Regional Revenue Share"
        )
        st.plotly_chart(
            chart_layout(fig),
            use_container_width=True
        )

    st.markdown("### Regional Summary")
    st.dataframe(
        regional,
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# SALES DATA PAGE
# --------------------------------------------------
elif page == "Sales Data":

    st.markdown(
        '<div class="section-title">Sales Transactions</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Explore the filtered records and export your results."
    )

    display_df = filtered_df.copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Revenue": st.column_config.NumberColumn(
                "Revenue (₹)", format="₹%.2f"
            ),
            "Unit_Price": st.column_config.NumberColumn(
                "Unit Price (₹)", format="₹%.2f"
            )
        }
    )

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Filtered Sales CSV",
        data=csv,
        file_name="filtered_sales_report.csv",
        mime="text/csv",
        use_container_width=True
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")

st.markdown("""
<div style="text-align:center;color:#8992A6;font-size:12px;padding:10px;">
    NOVA SALES INTELLIGENCE &nbsp; · &nbsp;
    Built with Python, Streamlit & Plotly
    <br><br>
    Thiranex Task 1 | Sales & Revenue Analysis Dashboard
</div>
""", unsafe_allow_html=True)