import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

st.set_page_config(page_title="E-commerce Analysis Dashboard", layout="wide")

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "main_data.csv")
    
    df = pd.read_csv(path)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

all_merged_df = load_data()
st.sidebar.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
st.sidebar.header("Filter Dashboard")

min_date = all_merged_df["order_purchase_timestamp"].min().date()
max_date = all_merged_df["order_purchase_timestamp"].max().date()

try:
    start_date, end_date = st.sidebar.date_input(
        "Rentang Waktu", 
        [min_date, max_date], 
        min_value=min_date, 
        max_value=max_date
    )
except ValueError:
    st.error("Silakan pilih rentang tanggal yang valid.")
    st.stop()

status_options = ["All"] + list(all_merged_df["order_status"].unique())
selected_status = st.sidebar.selectbox("Pilih Status Pesanan", status_options)

main_df = all_merged_df[
    (all_merged_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) &
    (all_merged_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))
]

if selected_status != "All":
    main_df = main_df[main_df["order_status"] == selected_status]

st.title("Analisis Data E-commerce 📊")
st.write(f"Menampilkan data dari **{start_date}** hingga **{end_date}** dengan status: **{selected_status}**")

st.header("Kategori Produk Terlaris & Terendah")
category_sales = main_df.groupby("product_category_name_english")["order_id"].nunique().reset_index()
category_sales.columns = ["product_category", "sales_volume"]

top_5 = category_sales.sort_values("sales_volume", ascending=False).head(5)
bottom_5 = category_sales.sort_values("sales_volume", ascending=True).head(5)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 5 Product Categories")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="sales_volume", y="product_category", data=top_5, palette="viridis", ax=ax)
    ax.set_xlabel("Jumlah Pesanan")
    ax.set_ylabel(None)
    st.pyplot(fig)

with col2:
    st.subheader("Bottom 5 Product Categories")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="sales_volume", y="product_category", data=bottom_5.sort_values("sales_volume", ascending=False), palette="magma", ax=ax)
    ax.set_xlabel("Jumlah Pesanan")
    ax.set_ylabel(None)
    ax.yaxis.tick_right()
    st.pyplot(fig)

st.header("Tren Pesanan Bulanan")
main_df["year"] = main_df["order_purchase_timestamp"].dt.year
main_df["month_str"] = main_df["order_purchase_timestamp"].dt.to_period("M").astype(str)

monthly_trend = main_df.groupby(["year", "month_str"])["order_id"].nunique().reset_index()
monthly_trend.columns = ["year", "month", "total_orders"]

fig, ax = plt.subplots(figsize=(16, 6))
sns.lineplot(
    data=monthly_trend, 
    x="month", 
    y="total_orders", 
    hue="year",     
    marker="o", 
    palette="flare", 
    ax=ax
)

plt.xticks(rotation=45)
plt.title("Jumlah Pesanan Bulanan (2016-2018)", fontsize=15)
plt.xlabel("Bulan")
plt.ylabel("Jumlah Pesanan")
plt.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

st.divider()
st.caption("Dione Raissa Ivana Matany | Informatics Engineering 2023 | UIN SGD Bandung")