import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

st.title('Analisis Data E-commerce: Volume Penjualan & Tren Pesanan')
st.write('Aplikasi ini menganalisis kategori produk terlaris/terlemah dan tren pesanan bulanan dari dataset e-commerce.')

# --- 1. Fungsi Pemuatan Data (ABSOLUTE PATH) ---
@st.cache_data
def load_data():
    base_path = "C:/Users/Dione/OneDrive/Dokumen/Analisis Data Dione Raissa Ivana Matany/Data"
    
    df_orders = pd.read_csv(f"{base_path}/orders_dataset.csv")
    df_items = pd.read_csv(f"{base_path}/order_items_dataset.csv")
    df_products = pd.read_csv(f"{base_path}/products_dataset.csv")
    df_category = pd.read_csv(f"{base_path}/product_category_name_translation.csv")
    
    return df_orders, df_items, df_products, df_category

# INI BARIS YANG TADI HILANG: Memanggil fungsinya
orders_df, order_items_df, products_df, category_translation_df = load_data()

st.subheader('1. Data Loaded (Sample)')
st.dataframe(orders_df.head(), use_container_width=True)

# --- 2. Fungsi Pembersihan Data ---
@st.cache_data
def clean_data(orders, items, products):
    datetime_cols = [
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_carrier_date", "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
    for col in datetime_cols:
        orders[col] = pd.to_datetime(orders[col], errors='coerce')

    items["shipping_limit_date"] = pd.to_datetime(items["shipping_limit_date"], errors='coerce')

    products["product_category_name"].fillna("unknown", inplace=True)
    numerical_cols = [
        "product_name_lenght", "product_description_lenght",
        "product_photos_qty", "product_weight_g",
        "product_length_cm", "product_height_cm", "product_width_cm"
    ]
    for col in numerical_cols:
        products[col].fillna(0, inplace=True)
        
    return orders, items, products

orders_df, order_items_df, products_df = clean_data(orders_df.copy(), order_items_df.copy(), products_df.copy())

st.subheader('2. Data Cleaning Status')
st.write("Data telah dibersihkan: Kolom tanggal dikonversi, nilai null di `products_df` diisi.")

# --- 3. Fungsi Penggabungan Data ---
@st.cache_data
def merge_data(orders, items, products, category):
    merged_1 = pd.merge(orders, items, on='order_id', how='inner')
    merged_2 = pd.merge(merged_1, products, on='product_id', how='inner')
    final_merged = pd.merge(merged_2, category, on='product_category_name', how='left')
    
    final_merged['order_purchase_timestamp'] = pd.to_datetime(final_merged['order_purchase_timestamp'])
    final_merged['purchase_year'] = final_merged['order_purchase_timestamp'].dt.year
    return final_merged

all_merged_df = merge_data(orders_df, order_items_df, products_df, category_translation_df)

st.subheader('3. Merged Data (Sample)')
st.dataframe(all_merged_df.head(), use_container_width=True)

# --- 4. Pertanyaan Bisnis 1: Kategori Produk ---
st.header('Pertanyaan Bisnis 1: Kategori Produk Terlaris dan Terlemah')

data_2016_2018 = all_merged_df[(all_merged_df['purchase_year'] >= 2016) & (all_merged_df['purchase_year'] <= 2018)]
category_sales = data_2016_2018.groupby('product_category_name_english')['order_id'].nunique().reset_index()
category_sales.columns = ['product_category', 'sales_volume']

top_5 = category_sales.sort_values(by='sales_volume', ascending=False).head(5)
bottom_5 = category_sales.sort_values(by='sales_volume', ascending=True).head(5)

col1, col2 = st.columns(2)
with col1:
    st.subheader('Top 5 Kategori (2016-2018)')
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(x='sales_volume', y='product_category', data=top_5, palette='viridis', ax=ax1)
    st.pyplot(fig1)

with col2:
    st.subheader('Bottom 5 Kategori (2016-2018)')
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(x='sales_volume', y='product_category', data=bottom_5, palette='magma', ax=ax2)
    st.pyplot(fig2)

# --- 5. Pertanyaan Bisnis 2: Tren Pesanan Bulanan ---
st.header('Pertanyaan Bisnis 2: Tren Pesanan Bulanan')

all_merged_df['purchase_month'] = all_merged_df['order_purchase_timestamp'].dt.to_period('M')
monthly_orders = all_merged_df.groupby(['purchase_year', 'purchase_month'])['order_id'].nunique().reset_index()
monthly_orders.columns = ['year', 'month', 'total_orders']
monthly_orders['month'] = monthly_orders['month'].astype(str)

fig3, ax3 = plt.subplots(figsize=(15, 6))
sns.lineplot(data=monthly_orders, x='month', y='total_orders', hue='year', marker='o', ax=ax3)
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(fig3)

# --- 6. RFM Analysis ---
st.header('Analisis Lanjutan: Persiapan RFM Analysis')
all_merged_df['total_item_price'] = all_merged_df['price'] + all_merged_df['freight_value']
current_date = all_merged_df['order_purchase_timestamp'].max()

rfm_df = all_merged_df.groupby('customer_id').agg(
    Recency=('order_purchase_timestamp', lambda date: (current_date - date.max()).days),
    Frequency=('order_id', 'nunique'),
    Monetary=('total_item_price', 'sum')
).reset_index()

st.dataframe(rfm_df.head(), use_container_width=True)
st.success('Alhamdulillah, Analisis Streamlit Jalan Sempurna! 🎉')