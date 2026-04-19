# Proyek Analisis Data: E-Commerce Public Dataset 🛍️

**Nama:** Dione Raissa Ivana Matany  
**Email:** dioneraissaim@gmail.com  
**ID Dicoding:** CDCC222D6X0575

## Gambaran Umum
Proyek ini menganalisis dataset publik e-commerce untuk mengidentifikasi pola penjualan, tren musiman, dan kategori produk berperforma tinggi/rendah. Tujuan utamanya adalah memberikan wawasan untuk optimasi manajemen inventaris dan strategi pemasaran.

## Pertanyaan Bisnis
1. Apa saja 5 kategori produk yang menghasilkan volume penjualan (jumlah pesanan) tertinggi dan terendah sepanjang periode 2016 hingga 2018 untuk mengoptimalkan manajemen inventaris?
2. Pada bulan apa terjadi lonjakan jumlah pesanan tertinggi setiap tahunnya (2016-2018), dan bagaimana tren pertumbuhan bulan-ke-bulan untuk menentukan waktu kampanye pemasaran yang paling efektif?

## Struktur Direktori
- `Dashboard/`: Berisi file `dashboard.py` dan data hasil pemrosesan.
- `Data/`: Berisi dataset mentah dalam format .csv.
- `Analisis_Data_Dione_Raissa_Ivana_Matany.ipynb`: File Jupyter Notebook untuk analisis data (Gathering hingga EDA).
- `README.md`: Dokumentasi proyek.
- `requirements.txt`: Daftar library python yang dibutuhkan.
- `url.txt`: Tautan dashboard jika sudah di-deploy.

## Metodologi Analisis
1. **Gathering Data:** Memuat dataset pesanan, produk, dan kategori.
2. **Assessing Data:** Memeriksa kualitas data, tipe data, dan missing values.
3. **Cleaning Data:** Konversi tipe datetime dan penanganan missing values pada atribut produk.
4. **Exploratory Data Analysis (EDA):** Menggabungkan dataset untuk menganalisis performa kategori produk dan tren waktu.
5. **Visualization:** Pembuatan Bar Chart untuk volume kategori dan Line Chart untuk tren pesanan bulanan.
6. **RFM Analysis:** Persiapan metrik Recency, Frequency, dan Monetary untuk segmentasi pelanggan.

## Hasil Analisis (Insight)
- **Performa Kategori:** Kategori `bed_bath_table` dan `health_beauty` mendominasi pasar, sementara kategori seperti `security_and_services` memerlukan evaluasi ulang strategi pemasaran.
- **Pola Musiman:** Terjadi lonjakan signifikan setiap akhir tahun (November) dan awal tahun (Januari), menunjukkan waktu krusial untuk meluncurkan promo besar.

## Cara Menjalankan Dashboard
Untuk menjalankan dashboard secara lokal, ikuti langkah berikut:

1. **Persiapan Environment:**
   Pastikan Anda memiliki Python terinstal dan disarankan menggunakan Virtual Environment.
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Untuk Windows
