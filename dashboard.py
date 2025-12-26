import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# ==========================================
# 1. SETUP & LOAD RESOURCES
# ==========================================
print("Memuat Sumber Daya ...")

# A. Load Model & Scaler
try:
    model = joblib.load('model_knn_smp.pkl')
    scaler = joblib.load('scaler_smp.pkl')
    print("Model dan Scaler berhasil dimuat!")
except FileNotFoundError:
    print("Error: File .pkl tidak ditemukan.")
    exit()

# B. Load Data Testing
try:
    df_test = pd.read_excel('DATASET/Data-Testing-Split.xlsx')
    print(f"Data Testing dimuat: {len(df_test)} siswa.")
except FileNotFoundError:
    print("Error: File 'DATASET/Data-Testing-Split.xlsx' tidak ditemukan.")
    exit()

# ==========================================
# 2. PREPROCESSING
# ==========================================
print("Menyiapkan Data Uji...")

# Ambil data mentah
X_test_raw = df_test.iloc[:, 1:5].values
y_test_true = df_test.iloc[:, 0].values

# NORMALISASI
X_test_scaled = scaler.transform(X_test_raw)

# ==========================================
# 3. EKSEKUSI PENGUJIAN (TESTING PHASE)
# ==========================================
print("Menjalankan simulasi ujian...")

results = []
hit_top6_count = 0
hit_top1_count = 0

# Prediksi Probabilitas
probs_all = model.predict_proba(X_test_scaled)
classes = model.classes_

# Loop Analisis Per Siswa
for i in range(len(df_test)):
    student_probs = probs_all[i]
    
    # Sorting Ranking
    sorted_idx = np.argsort(student_probs)[::-1]
    
    # Ambil Top 6
    top6_schools = classes[sorted_idx[:6]]
    top1_school = top6_schools[0]
    top1_conf = student_probs[sorted_idx[0]]
    
    real_school = y_test_true[i]
    
    # Cek Validitas
    is_hit_top6 = real_school in top6_schools
    is_hit_top1 = real_school == top1_school
    
    if is_hit_top6: hit_top6_count += 1
    if is_hit_top1: hit_top1_count += 1
    
    # Simpan Data untuk Laporan Excel
    results.append({
        'Siswa_ID': i+1,
        'Sekolah_Asli': real_school,
        'Nilai_Input': str(X_test_raw[i]),
        'Rekomendasi_1': top1_school,
        'Confidence_1': round(top1_conf, 4),
        'Status_Top6': 'BERHASIL' if is_hit_top6 else 'MELESET',
        'List_Rekomendasi': ", ".join(top6_schools)
    })

df_results = pd.DataFrame(results)

# ==========================================
# 4. VISUALISASI DASHBOARD FINAL
# ==========================================
print("Membuat Dashboard Laporan Testing...")

fig, axes = plt.subplots(2, 2, figsize=(18, 12))
plt.suptitle(f"EVALUASI MODEL", fontsize=20, fontweight='bold')

# A. PIE CHART: Akurasi Top-6
labels = ['BERHASIL (Top-6)', 'MELESET']
sizes = [hit_top6_count, len(df_test) - hit_top6_count]
colors = ['#27ae60', '#c0392b'] 
axes[0, 0].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=(0.1, 0))
axes[0, 0].set_title('Akurasi Sistem Rekomendasi (Top-6)', fontsize=14)

# B. BAR CHART: Distribusi Rekomendasi Top-1
top_recs = df_results['Rekomendasi_1'].value_counts().head(10)
sns.barplot(x=top_recs.values, y=top_recs.index, ax=axes[0, 1], palette='viridis')
axes[0, 1].set_title('10 Sekolah Paling Sering Direkomendasikan (Top-1)', fontsize=14)
axes[0, 1].set_xlabel('Frekuensi')

# C. HISTOGRAM: Confidence Score
sns.histplot(df_results['Confidence_1'], bins=20, kde=True, ax=axes[1, 0], color='#2980b9')
axes[1, 0].set_title('Distribusi Keyakinan Model (Confidence)', fontsize=14)
axes[1, 0].set_xlabel('Probabilitas')

# D. KARTU NILAI (REAL ACCURACY)
acc_top6 = (hit_top6_count / len(df_test)) * 100
acc_top1 = (hit_top1_count / len(df_test)) * 100

summary_text = f"""
LAPORAN PENGUJIAN FINAL (JUJUR):
--------------------------------
Total Data Uji     : {len(df_test)} Siswa

✅ Top-6 Accuracy  : {acc_top6:.2f}%
(Validitas Sistem Rekomendasi)

⚠️ Top-1 Accuracy  : {acc_top1:.2f}%
(Prediksi Tunggal)

Fitur yang Digunakan:
Hanya Rata-rata Mapel (PKN, IND, MTK, IPA)
"""
axes[1, 1].text(0.05, 0.5, summary_text, fontsize=14, fontfamily='monospace', va='center', 
                bbox=dict(facecolor='#ecf0f1', alpha=0.8, boxstyle='round,pad=1'))
axes[1, 1].axis('off')

# Simpan Output
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('Dashboard_Final_Testing.png')
print("Gambar Dashboard disimpan: 'Dashboard_Final_Testing.png'")

df_results.to_excel('Laporan_Detail_Testing.xlsx', index=False)
print("Excel Laporan disimpan: 'Laporan_Detail_Testing.xlsx'")