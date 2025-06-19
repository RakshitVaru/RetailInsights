import streamlit as st
import pandas as pd
import requests

import os
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Retail Insights Dashboard", layout="wide")
st.title("📊 Retail Insights Dashboard")

# Upload CSV file to backend
st.sidebar.header("Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
    with st.spinner("Uploading and processing..."):
        res = requests.post(f"{API_URL}/upload/", files=files)
    if res.status_code == 200:
        st.sidebar.success("File uploaded and processed!")
    else:
        st.sidebar.error("Upload failed: " + res.json().get("detail", "Unknown error"))

# Show Total Revenue
st.header("Key Metrics")
revenue_res = requests.get(f"{API_URL}/sales/total")
if revenue_res.status_code == 200:
    total_revenue = revenue_res.json().get("total_revenue", 0)
    st.metric(label="💰 Total Revenue", value=f"${total_revenue:,.2f}")
else:
    st.warning("Could not fetch total revenue")

# Show Top Selling Items
top_items_res = requests.get(f"{API_URL}/sales/top-items")
if top_items_res.status_code == 200:
    top_items_json = top_items_res.json()
    top_items_df = pd.DataFrame(top_items_json)
    if not top_items_df.empty and "item" in top_items_df.columns:
        st.subheader("🏆 Top Selling Items")
        st.bar_chart(top_items_df.set_index("item"))
    else:
        st.info("No item data available.")
else:
    st.warning("Could not load top items")


# Show Sales by Category
category_res = requests.get(f"{API_URL}/sales/by-category")
if category_res.status_code == 200:
    category_json = category_res.json()
    category_df = pd.DataFrame(category_json)

    if not category_df.empty:
        st.subheader("📦 Revenue by Category")
        if "category" in category_df.columns and "revenue" in category_df.columns:
            st.bar_chart(category_df.set_index("category")["revenue"])
            st.dataframe(category_df)
        else:
            st.warning("Expected columns 'category' and 'revenue' not found in response.")
    else:
        st.info("No category sales data available.")
else:
    st.error("Failed to fetch category data.")
