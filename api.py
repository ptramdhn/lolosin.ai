from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib
import os

# ==========================================
# 1. SETUP API & MODEL
# ==========================================
app = FastAPI(
    title="Lolosin.ai API - SMPN Jakut",
    description="Backend API untuk sistem rekomendasi sekolah berbasis k-NN.",
    version="2.0.0"
)

print("Memuat Otak AI (Model & Scaler)...")
try:
    model = joblib.load('model_knn_smp.pkl')
    scaler = joblib.load('scaler_smp.pkl')
    print("✅ Model berhasil dimuat!")
except FileNotFoundError:
    print("❌ FATAL ERROR: File model_knn_smp.pkl atau scaler_smp.pkl tidak ditemukan.")
    raise RuntimeError("Model files not found. Please run training script first.")

# ==========================================
# 2. DEFINISI STRUKTUR DATA (Pydantic)
# ==========================================
# Ini seperti formulir pemesanan, memastikan data yang masuk sesuai standar.
class RaporInput(BaseModel):
    # List nilai per mapel (Semester 1 s.d. 5)
    pkn_scores: list[float]
    ind_scores: list[float]
    mat_scores: list[float]
    ipa_scores: list[float]

    class Config:
        # Contoh data untuk dokumentasi API (Swagger UI)
        json_schema_extra = {
            "example": {
                "pkn_scores": [85.0, 86.0, 85.0, 87.0, 88.0],
                "ind_scores": [88.0, 89.0, 88.0, 88.0, 89.0],
                "mat_scores": [90.0, 90.0, 92.0, 91.0, 92.0],
                "ipa_scores": [89.0, 90.0, 90.0, 91.0, 90.0]
            }
        }

# ==========================================
# 3. ENDPOINT API
# ==========================================

@app.get("/")
def read_root():
    return {"status": "online", "message": "Lolosin.ai API is running smooth!"}

@app.post("/predict")
def predict_school(data: RaporInput):
    """
    Menerima 5 nilai per mapel, menghitung rata-rata, dan mengembalikan 6 rekomendasi sekolah.
    """
    try:
        # A. Validasi Input
        # Pastikan setiap mapel punya tepat 5 nilai (Kls 4 Smt 1 s.d. Kls 6 Smt 1)
        if any(len(scores) != 5 for scores in [data.pkn_scores, data.ind_scores, data.mat_scores, data.ipa_scores]):
            raise HTTPException(status_code=400, detail="Setiap mata pelajaran harus memiliki tepat 5 nilai semester.")

        # B. Hitung Rata-rata (Preprocessing)
        avg_pkn = np.mean(data.pkn_scores)
        avg_ind = np.mean(data.ind_scores)
        avg_mat = np.mean(data.mat_scores)
        avg_ipa = np.mean(data.ipa_scores)
        
        # C. Hitung Statistik Tambahan (Untuk Info Visual di Frontend)
        base_features = np.array([avg_pkn, avg_ind, avg_mat, avg_ipa])
        consistency = np.std(base_features)
        min_score = np.min(base_features)

        # D. Prediksi AI
        # Siapkan data input model (Hanya 4 Rata-rata Murni)
        final_input = np.array([[avg_pkn, avg_ind, avg_mat, avg_ipa]])
        # Normalisasi
        input_scaled = scaler.transform(final_input)
        # Minta model berpikir
        probs = model.predict_proba(input_scaled)[0]
        classes = model.classes_

        # E. Ambil Top 6 Hasil
        sorted_indices = np.argsort(probs)[::-1][:6]
        
        recommendations = []
        for idx in sorted_indices:
            recommendations.append({
                "school_name": classes[idx],
                "probability": float(probs[idx]) # Ubah ke float biar bisa jadi JSON
            })

        # F. Kirim Balasan ke Frontend
        return {
            "status": "success",
            "statistics": {
                "avg_pkn": float(avg_pkn),
                "avg_ind": float(avg_ind),
                "avg_mat": float(avg_mat),
                "avg_ipa": float(avg_ipa),
                "consistency_std": float(consistency),
                "min_score": float(min_score)
            },
            "recommendations": recommendations
        }

    except Exception as e:
        # Tangkap error tak terduga
        print(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# 4. CARA MENJALANKAN
# ==========================================
# Di terminal, jalankan perintah:
# uvicorn api:app --reload
#
# --reload artinya server akan restart otomatis kalau ada perubahan di kodenya.
# API akan jalan di http://127.0.0.1:8000
# Dokumentasi ada di http://127.0.0.1:8000/docs