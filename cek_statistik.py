import pandas as pd

# 1. Load Data Asli
try:
    # Sesuaikan nama file jika berbeda
    df = pd.read_excel('DATASET/Data-Cleaning.xlsx')
    print("✅ Data Berhasil Dimuat!")
except FileNotFoundError:
    print("❌ File tidak ditemukan. Pastikan path 'DATASET/Data-Cleaning.xlsx' benar.")
    exit()

# 2. Pilih Kolom Nilai Rapor
target_columns = ['Rerata_Smt_PKN', 'Rerata_Smt_BIND', 'Rerata_Smt_MAT', 'Rerata_Smt_IPA']

try:
    # Ambil hanya kolom nilai
    df_nilai = df[target_columns]

    # 3. Hitung Statistik Deskriptif
    stats = df_nilai.describe().T # .T artinya ditranspose (dibalik baris jadi kolom)
    
    final_stats = stats[['mean', 'std', 'min', 'max']]
    
    # Rename kolom biar bahasa Indonesia 
    final_stats.columns = ['Rata-rata (Mean)', 'Standar Deviasi', 'Nilai Min', 'Nilai Max']

    print("\n" + "="*50)
    print("📊 STATISTIK DESKRIPTIF (BAB 4.1.1)")
    print("="*50)
    print(final_stats.round(2)) # Bulatkan 2 angka di belakang koma
    print("="*50)

    # Simpan ke Excel 
    final_stats.round(2).to_excel("Laporan_Statistik.xlsx")
    print("\n✅ Hasil juga disimpan ke file 'Laporan_Statistik.xlsx'")

except KeyError as e:
    print(f"\n❌ Error: Nama kolom tidak sesuai. Cek nama kolom di Excel.")
    print(f"Detail error: {e}")
    print("Nama kolom yang ada di file:", df.columns.tolist())