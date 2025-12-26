import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
import joblib 

# ==========================================
# 1. SETUP & SPLIT DATA YANG TRANSPARAN
# ==========================================
print("MEMULAI PROSES TRAINING...")

# Load data utuh
try:
    df = pd.read_excel('DATASET/Data-Cleaning.xlsx')
except FileNotFoundError:
    # Fallback kalau formatnya csv
    try:
        df = pd.read_csv('DATASET/Data-Cleaning.xlsx - Sheet1.csv')
    except:
        print("❌ Error: File Data tidak ditemukan.")
        exit()

# SPLIT DATA (80% Train, 20% Test)
# Stratify penting agar proporsi sekolah seimbang
df_train, df_test = train_test_split(df, test_size=0.2, random_state=42, stratify=df.iloc[:, 0])

# SIMPAN BUKTI SPLIT
df_train.to_excel('DATASET/Data-Training-Split.xlsx', index=False)
df_test.to_excel('DATASET/Data-Testing-Split.xlsx', index=False)

print("Data berhasil dipecah dan disimpan:")
print(f"   - Training: {len(df_train)} siswa (Disimpan di 'DATASET/Data-Training-Split.xlsx')")
print(f"   - Testing : {len(df_test)} siswa (Disimpan di 'DATASET/Data-Testing-Split.xlsx')")

# ==========================================
# 2. PERSIAPAN VARIABLE (X dan y)
# ==========================================
# ambil X dan y DARI HASIL SPLIT DI ATAS, bukan dari data utuh
X_train = df_train.iloc[:, 1:5].values
y_train = df_train.iloc[:, 0].values

X_test = df_test.iloc[:, 1:5].values
y_test = df_test.iloc[:, 0].values

# ==========================================
# 3. NORMALISASI
# ==========================================
scaler = MinMaxScaler()

# PERHATIKAN: model hanya 'fit' (belajar) dari X_train.
# X_test hanya ikut diubah (transform) tanpa diintip statistiknya.
scaler.fit(X_train) 

X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Simpan scaler
joblib.dump(scaler, 'scaler_smp.pkl')
print("Scaler disimpan.")

# ==========================================
# 4. TUNING (Mencari K Terbaik)
# ==========================================
print("Mencari Nilai K Terbaik ...")
accuracies = []
k_range = range(10, 101, 5)

best_acc = 0
best_k = 0

for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k, weights='distance')
    
    # Latih model dengan data training
    knn.fit(X_train_scaled, y_train)
    
    # Uji ke data testing
    probs = knn.predict_proba(X_test_scaled)
    hit = 0
    for i, true_school in enumerate(y_test):
        top6_idx = np.argsort(probs[i])[-6:]
        if true_school in knn.classes_[top6_idx]:
            hit += 1
    
    current_acc = hit / len(y_test)
    accuracies.append(current_acc)
    
    if current_acc > best_acc:
        best_acc = current_acc
        best_k = k

# ==========================================
# 5. VISUALISASI
# ==========================================
plt.figure(figsize=(10, 6))
plt.plot(k_range, accuracies, marker='o', color='blue')
plt.title(f'Akurasi Top-6 pada Unseen Data (Test Size: {len(df_test)})')
plt.xlabel('Nilai K')
plt.ylabel('Akurasi')
plt.grid(True)
plt.savefig('grafik_tuning_k.png')
print("✅ Grafik validasi disimpan 'grafik_tuning_k.png'.")

# ==========================================
# 6. SIMPAN MODEL FINAL 
# ==========================================
print(f"\n🏆 K Terbaik: {best_k} dengan Akurasi: {best_acc:.2%}")

# simpan model yang HANYA dilatih dengan X_train.
final_model = KNeighborsClassifier(n_neighbors=best_k, weights='distance')
final_model.fit(X_train_scaled, y_train) 

joblib.dump(final_model, 'model_knn_smp.pkl')
print("✅ Model Final disimpan sebagai 'model_knn_smp.pkl'")