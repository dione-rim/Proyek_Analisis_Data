import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="E-commerce Analysis Dashboard", layout="wide")

# --- 1. Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("Dashboard/main_data.csv")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

all_merged_df = load_data()

# --- 2. Sidebar Filters ---
st.sidebar.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
st.sidebar.header("Filter Dashboard")

# Kontrol 1: Date Input
min_date = all_merged_df["order_purchase_timestamp"].min().date()
max_date = all_merged_df["order_purchase_timestamp"].max().date()
start_date, end_date = st.sidebar.date_input(
    "Rentang Waktu", [min_date, max_date], min_value=min_date, max_value=max_date
)

# Kontrol 2: Selectbox untuk Order Status
status_options = ["All"] + list(all_merged_df["order_status"].unique())
selected_status = st.sidebar.selectbox("Pilih Status Pesanan", status_options)

# --- 3. Filtering Logic ---
main_df = all_merged_df[
    (all_merged_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) &
    (all_merged_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))
]

if selected_status != "All":
    main_df = main_df[main_df["order_status"] == selected_status]

# --- 4. Main Dashboard UI ---
st.title("Analisis Data E-commerce 📊")

# Visualization 1: Product Categories (TIDAK BERUBAH)
st.header("Kategori Produk Terlaris & Terendah")
category_sales = main_df.groupby("product_category_name_english")["order_id"].nunique().reset_index()
category_sales.columns = ["product_category", "sales_volume"]

top_5 = category_sales.sort_values("sales_volume", ascending=False).head(5)
bottom_5 = category_sales.sort_values("sales_volume", ascending=True).head(5)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 5 Product Categories")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="sales_volume", y="product_category", data=top_5, palette="Blues_r", ax=ax)
    ax.set_xlabel("Jumlah Pesanan")
    ax.set_ylabel(None)
    st.pyplot(fig)

with col2:
    st.subheader("Bottom 5 Product Categories")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="sales_volume", y="product_category", data=bottom_5.sort_values("sales_volume", ascending=False), palette="Reds_r", ax=ax)
    ax.set_xlabel("Jumlah Pesanan")
    ax.set_ylabel(None)
    ax.yaxis.tick_right()
    st.pyplot(fig)

# --- BAGIAN YANG DIUBAH AGAR SESUAI GAMBAR 1 ---
# Visualization 2: Monthly Trend
st.header("Tren Pesanan Bulanan")

# Tambahkan kolom tahun untuk 'hue'
main_df["year"] = main_df["order_purchase_timestamp"].dt.year
main_df["month_year"] = main_df["order_purchase_timestamp"].dt.to_period("M").astype(str)

# Grouping agar ada informasi tahun
monthly_trend = main_df.groupby(["year", "month_year"])["order_id"].nunique().reset_index()
monthly_trend.columns = ["year", "month_year", "total_orders"]

fig, ax = plt.subplots(figsize=(16, 6))
sns.lineplot(
    data=monthly_trend, 
    x="month_year", 
    y="total_orders", 
    hue="year",       # Memberikan warna berbeda tiap tahun sesuai Gambar 1
    marker="o", 
    palette="flare",   # Palet flare/magma agar mirip warna ungu-pink di Colab
    ax=ax
)

plt.xticks(rotation=45)
plt.title("Jumlah Pesanan Bulanan (2016-2018)", fontsize=15)
plt.xlabel("Bulan")
plt.ylabel("Jumlah Pesanan")
plt.grid(True, linestyle='--', alpha=0.7) # Menambahkan grid sesuai Gambar 1
st.pyplot(fig)

st.caption("Dione Raissa Ivana Matany 2026")