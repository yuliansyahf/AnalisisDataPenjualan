import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

# 1. Load Data
# Pastikan file csv berada di folder yang sama dengan skrip ini
df = pd.read_csv('data_praktikum_analisis_data.csv')

# 2. Data Cleaning & Wrangling
# Membersihkan data harga yang tidak valid
df = df[df['Price_Per_Unit'] > 0]
# Mengubah kolom tanggal menjadi tipe datetime
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# # --- VISUALISASI TREN PENJUALAN BULANAN ---
# df['Month'] = df['Order_Date'].dt.to_period('M').astype(str)
# monthly_sales = df.groupby('Month')['Total_Sales'].sum()

# plt.figure(figsize=(10,5))
# plt.plot(monthly_sales.index, monthly_sales.values, marker='o', color='b')
# plt.title('Tren Penjualan Bulanan')
# plt.xticks(rotation=45)
# plt.savefig('tren_penjualan.png', bbox_inches='tight') # Simpan gambar tren
# plt.show()

# --- ANALISIS KORELASI (HEATMAP) ---
correlation = df[['Total_Sales','Ad_Budget', 'Price_Per_Unit']].corr()
plt.figure(figsize=(8,6))
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title('Peta Korelasi Antar Variabel')
plt.savefig('heatmap_korelasi.png', bbox_inches='tight') # Simpan gambar heatmap
plt.show()

# # --- TUGAS 1: IDENTIFIKASI PRODUK UNDERPERFORMER ---
# avg_price = df['Price_Per_Unit'].mean()
# # Produk dengan harga di atas rata-rata tapi kuantitas rendah
# plt.figure(figsize=(10, 6))
# sns.scatterplot(data=df, x='Price_Per_Unit', y='Quantity', hue='Product_Category')
# plt.axvline(avg_price, color='red', linestyle='--', label='Rata-rata Harga')
# plt.title('Scatter Plot: Harga vs Kuantitas (Mencari Underperformer)')
# plt.legend()
# plt.savefig('tugas1_underperformer.png', bbox_inches='tight') # Simpan gambar tugas 1
# plt.show()

# # --- TUGAS 2: SEGMENTASI PELANGGAN (RFM ANALYSIS) ---
# # Menghitung Recency, Frequency, dan Monetary
# snapshot_date = df['Order_Date'].max() + dt.timedelta(days=1)

# rfm = df.groupby('CustomerID').agg({
#     'Order_Date': lambda x: (snapshot_date - x.max()).days, # Recency
#     'Order_ID': 'count',                                   # Frequency
#     'Total_Sales': 'sum'                                   # Monetary
# })

# rfm.columns = ['Recency', 'Frequency', 'Monetary']

# # Memberikan skor 1-5
# rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
# rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
# rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

# rfm['RFM_Segment'] = rfm.R_Score.astype(str) + rfm.F_Score.astype(str) + rfm.M_Score.astype(str)
# print("\nHasil Segmentasi RFM (5 Teratas):")
# print(rfm.head())

# # --- TUGAS 3: ANALISIS KONTRIBUSI KATEGORI (EFISIENSI IKLAN) ---
# category_analysis = df.groupby('Product_Category').agg({
#     'Total_Sales': 'sum',
#     'Ad_Budget': 'sum'
# })
# # Menghitung rasio efisiensi iklan
# category_analysis['Efficiency'] = category_analysis['Total_Sales'] / category_analysis['Ad_Budget']
# category_analysis = category_analysis.sort_values(by='Efficiency')

# plt.figure(figsize=(10, 5))
# category_analysis['Efficiency'].plot(kind='barh', color='teal')
# plt.title('Efisiensi Kategori (Penjualan per Rupiah Iklan)')
# plt.xlabel('Rasio Efisiensi')
# plt.savefig('tugas3_efisiensi.png', bbox_inches='tight') # Simpan gambar tugas 3
# plt.show()

# # --- TUGAS 4: UJI HIPOTESIS SEDERHANA (PENGARUH IKLAN) ---
# median_ads = df['Ad_Budget'].median()
# high_ads = df[df['Ad_Budget'] > median_ads]['Total_Sales']
# low_ads = df[df['Ad_Budget'] <= median_ads]['Total_Sales']

# print(f"\nRata-rata Penjualan Iklan Tinggi: {high_ads.mean():.2f}")
# print(f"Rata-rata Penjualan Iklan Rendah: {low_ads.mean():.2f}")

# if high_ads.mean() > low_ads.mean():
#     print("Kesimpulan: Peningkatan Ad_Budget cenderung menghasilkan penjualan lebih tinggi.")
# else:
#     print("Kesimpulan: Ad_Budget tidak berpengaruh signifikan secara rata-rata.")