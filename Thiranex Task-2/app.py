import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    layout="wide"
)

st.title("Customer Segmentation Dashboard")
st.write("Analyze customer income and spending behavior.")

# Sample customer data
data = {
    "CustomerID": range(1, 21),
    "AnnualIncome": [
        15, 18, 20, 22, 25,
        35, 38, 40, 45, 48,
        55, 58, 60, 65, 68,
        75, 80, 85, 90, 95
    ],
    "SpendingScore": [
        85, 90, 78, 82, 75,
        40, 45, 50, 42, 48,
        65, 70, 60, 68, 62,
        25, 30, 20, 35, 28
    ]
}

df = pd.DataFrame(data)

# Sidebar controls
st.sidebar.header("Dashboard Settings")
clusters = st.sidebar.slider(
    "Number of customer segments",
    min_value=2,
    max_value=5,
    value=3
)

# Perform clustering
features = df[["AnnualIncome", "SpendingScore"]]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

model = KMeans(
    n_clusters=clusters,
    random_state=42,
    n_init=10
)

df["Segment"] = model.fit_predict(scaled_features)

# Dashboard metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", len(df))
col2.metric("Customer Segments", clusters)
col3.metric(
    "Average Spending Score",
    round(df["SpendingScore"].mean(), 1)
)

st.divider()

# Customer segmentation chart
st.subheader("Customer Segmentation Chart")

fig, ax = plt.subplots()

for segment in sorted(df["Segment"].unique()):
    group = df[df["Segment"] == segment]
    ax.scatter(
        group["AnnualIncome"],
        group["SpendingScore"],
        label=f"Segment {segment}",
        s=80
    )

ax.set_xlabel("Annual Income (in thousands)")
ax.set_ylabel("Spending Score (0-100)")
ax.set_title("Customer Groups")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)
plt.close(fig)

# Customer data table
st.subheader("Customer Details")
st.dataframe(df, use_container_width=True)

# Download results
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Customer Segments CSV",
    data=csv,
    file_name="customer_segments.csv",
    mime="text/csv"
)