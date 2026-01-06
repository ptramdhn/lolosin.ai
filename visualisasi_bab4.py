import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load Data
try:
    df = pd.read_excel('DATASET/Data-Cleaning.xlsx')
    print("✅ Data berhasil dimuat!")
except FileNotFoundError:
    print("❌ File tidak ditemukan. Cek path 'DATASET/Data-Cleaning.xlsx'")
    exit()

# 2. Pilih Kolom Nilai Saja
cols = ['Rerata_Smt_PKN', 'Rerata_Smt_BIND', 'Rerata_Smt_MAT', 'Rerata_Smt_IPA']
df_corr = df[cols]

# Ganti nama kolom biar bagus di gambar
df_corr.columns = ['PKN', 'B.Ind', 'MTK', 'IPA']

# 3. Hitung Korelasi
correlation_matrix = df_corr.corr()

# 4. Buat Gambar Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(
    correlation_matrix, 
    annot=True,           # Tampilkan angkanya
    cmap='coolwarm',      # Warna (Biru ke Merah)
    fmt=".2f",            # 2 angka di belakang koma
    linewidths=0.5,       # Garis pemisah
    vmin=0, vmax=1        # Skala 0 sampai 1
)

plt.title('Korelasi Antar Mata Pelajaran', fontsize=14, fontweight='bold')
plt.tight_layout()

# 5. Simpan Gambar
nama_file = "heatmap_korelasi.png"
plt.savefig(nama_file, dpi=300)
print(f"✅ Gambar berhasil disimpan sebagai '{nama_file}'")

# Tampilkan di layar juga
plt.show()