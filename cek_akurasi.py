import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

# ==========================================
# SCRIPT CEK AKURASI
# ==========================================

def get_top_n_accuracy(model, X, y, n=6):
    """Fungsi hitung akurasi Top-N"""
    probs = model.predict_proba(X)
    classes = model.classes_
    
    hits = 0
    for i in range(len(y)):
        # Ambil indeks N probabilitas tertinggi
        top_n_idx = np.argsort(probs[i])[-n:]
        # Cek apakah kelas asli ada di top N prediksi
        if y[i] in classes[top_n_idx]:
            hits += 1
    return hits / len(y)

# 1. Load Data Asli
print("📂 Memuat data...")
try:
    df = pd.read_excel('DATASET/Data-Cleaning.xlsx')
except FileNotFoundError:
    print("❌ File 'DATASET/Data-Cleaning.xlsx' tidak ditemukan.")
    exit()

# 2. Split Data 
# Pastikan random_state=42 (sesuai standar)
X = df.iloc[:, 1:5].values  # Kolom Nilai
y = df.iloc[:, 0].values    # Kolom Sekolah

# Split 80:20
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"✅ Data Uji siap: {len(X_test)} sampel")

# 3. Load Model Utama (k-NN)
try:
    knn_model = joblib.load('model_knn_smp.pkl')
    scaler = joblib.load('scaler_smp.pkl')
    
    # Normalisasi Data Uji (Penting!)
    X_test_scaled = scaler.transform(X_test)
    X_train_scaled = scaler.transform(X_train) # Untuk RF nanti
    
    print("✅ Model k-NN berhasil dimuat.")
except FileNotFoundError:
    print("❌ Model .pkl belum ada. Jalankan training dulu!")
    exit()

# 4. Hitung Akurasi k-NN (Model Utama)
print("\n🧮 Menghitung Akurasi k-NN...")
acc_knn_top1 = accuracy_score(y_test, knn_model.predict(X_test_scaled))
acc_knn_top6 = get_top_n_accuracy(knn_model, X_test_scaled, y_test, n=6)

# 5. Latih Random Forest (Sebagai Pembanding di Tabel)
# latih sebentar RF biar punya data pembanding yang valid
print("🌲 Melatih Random Forest (untuk pembanding)...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)

acc_rf_top1 = accuracy_score(y_test, rf_model.predict(X_test_scaled))
acc_rf_top6 = get_top_n_accuracy(rf_model, X_test_scaled, y_test, n=6)

# 7. TAMPILKAN HASIL
print("\n" + "="*70)
print("📊 HASIL AKHIR")
print("="*70)
print(f"{'Model / Metode':<35} | {'Top-1 Accuracy':<15} | {'Top-6 Accuracy':<15}")
print("-" * 70)
print(f"{'1. Random Forest (Pembanding)':<35} | {acc_rf_top1:.2%}          | {acc_rf_top6:.2%}")
print(f"{'2. k-NN Standard (Model Kita)':<35} | {acc_knn_top1:.2%}          | {acc_knn_top6:.2%}")
print("="*70)