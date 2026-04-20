import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

# --- 1. Fungsi Pemuatan Data ---
@st.cache_data
def load_data():
    df_orders = pd.read_csv("Data/orders_dataset.csv")
    df_items = pd.read_csv("Data/order_items_dataset.csv")
    df_products = pd.read_csv("Data/products_dataset.csv")
    df_category = pd.read_csv("Data/product_category_name_translation.csv")
    return df_orders, df_items, df_products, df_category

# --- 2. Fungsi Pembersihan Data ---
@st.cache_data
def clean_data(orders, items, products):
    datetime_cols = ["order_purchase_timestamp", "order_approved_at", "order_delivered_customer_date"]
    for col in datetime_cols:
        orders[col] = pd.to_datetime(orders[col], errors='coerce')
    products["product_category_name"].fillna("unknown", inplace=True)
    return orders, items, products

# --- LOAD DATA ---
raw_orders, raw_items, raw_products, category_translation_df = load_data()
orders_df, order_items_df, products_df = clean_data(raw_orders.copy(), raw_items.copy(), raw_products.copy())

# --- MERGE DATA ---
merged_df = pd.merge(orders_df, order_items_df, on='order_id', how='inner')
merged_df = pd.merge(merged_df, products_df, on='product_id', how='inner')
all_merged_df = pd.merge(merged_df, category_translation_df, on='product_category_name', how='left')

# ==========================================
# SIDEBAR FILTER (INI YANG DIMINTA REVIEWER)
# ==========================================
st.sidebar.header("Filter Dashboard")

# Filter Rentang Tanggal
min_date = all_merged_df["order_purchase_timestamp"].min().date()
max_date = all_merged_df["order_purchase_timestamp"].max().date()

start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Menghubungkan Filter ke Dataframe
main_df = all_merged_df[(all_merged_df["order_purchase_timestamp"] >= str(start_date)) & 
                       (all_merged_df["order_purchase_timestamp"] <= str(end_date))]

# ==========================================
# MAIN DASHBOARD
# ==========================================
st.title('Analisis Data E-commerce 📊')

# Pertanyaan 1: Kategori Produk
st.header('Kategori Produk Terlaris dan Terlemah')

category_sales = main_df.groupby('product_category_name_english')['order_id'].nunique().reset_index()
category_sales.columns = ['product_category', 'sales_volume']

top_5 = category_sales.sort_values(by='sales_volume', ascending=False).head(5)
bottom_5 = category_sales.sort_values(by='sales_volume', ascending=True).head(5)

col1, col2 = st.columns(2)
with col1:
    st.subheader('Top 5 Kategori')
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(x='sales_volume', y='product_category', data=top_5, palette='viridis', ax=ax1)
    st.pyplot(fig1)

with col2:
    st.subheader('Bottom 5 Kategori')
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(x='sales_volume', y='product_category', data=bottom_5, palette='magma', ax=ax2)
    st.pyplot(fig2)

# Pertanyaan 2: Tren Pesanan
st.header('Tren Pesanan Bulanan')
main_df['month'] = main_df['order_purchase_timestamp'].dt.to_period('M').astype(str)
monthly_orders = main_df.groupby('month')['order_id'].nunique().reset_index()

fig3, ax3 = plt.subplots(figsize=(15, 6))
sns.lineplot(data=monthly_orders, x='month', y='order_id', marker='o', ax=ax3)
plt.xticks(rotation=45)
st.pyplot(fig3)

st.success(f'Data ditampilkan untuk rentang {start_date} hingga {end_date}')