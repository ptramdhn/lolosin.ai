import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ==========================================
# 1. KONFIGURASI & STYLE
# ==========================================
st.set_page_config(
    page_title="Lolosin.ai - Mode Cepat",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
<style>
    .stNumberInput {margin-bottom: 15px;}
    
    .main-header {
        font-size: 2.5rem; 
        font-weight: 700; 
        color: #1E88E5; 
        margin-bottom: 0;
    }
    
    .tagline {
        font-size: 1.2rem; 
        font-style: italic; 
        opacity: 0.8; 
        margin-bottom: 20px;
    }
    
    .info-box {
        background-color: #e3f2fd; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #1E88E5; 
        margin-bottom: 25px;
        color: #000000;
    }
    
    .disclaimer {
        font-size: 0.8rem; 
        opacity: 0.7; 
        text-align: center; 
        margin-top: 30px; 
        border-top: 1px solid #eee; 
        padding-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOAD MODEL & SCALER
# ==========================================
@st.cache_resource
def load_resources():
    try:
        model = joblib.load('model_knn_smp.pkl')
        scaler = joblib.load('scaler_smp.pkl')
        return model, scaler
    except FileNotFoundError:
        return None, None

model, scaler = load_resources()

if model is None:
    st.error("❌ File Model tidak ditemukan!")
    st.stop()

# ==========================================
# 3. HEADER & INPUT FORM
# ==========================================
st.markdown('<p class="main-header">⚡ Lolosin.ai (Quick Mode)</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Input Rata-rata Langsung. Kata AI, bukan katanya.</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>📋 Mode Input Cepat:</strong><br>
    Gunakan mode ini jika kamu sudah memiliki <b>Nilai Rata-Rata Akhir.</b>
    Masukkan angka rata-rata langsung ke dalam kolom di bawah.
</div>
""", unsafe_allow_html=True)

# Container Input (2 Kolom Rapi)
col1, col2 = st.columns(2)

with col1:
    pkn = st.number_input("Rata-rata PKN", 0.0, 100.0, 85.0, step=0.1, help="Nilai rata-rata akumulasi 5 semester")
    ind = st.number_input("Rata-rata B. Indonesia", 0.0, 100.0, 85.0, step=0.1)

with col2:
    mat = st.number_input("Rata-rata Matematika", 0.0, 100.0, 85.0, step=0.1)
    ipa = st.number_input("Rata-rata IPA", 0.0, 100.0, 85.0, step=0.1)

st.markdown("---")

# ==========================================
# 4. LOGIKA PREDIKSI
# ==========================================
if st.button("🔍 Analisis & Cari Rekomendasi", type="primary"):
    
    # A. Siapkan Data Input (Hanya 4 Kolom)
    # Urutan harus: [PKN, IND, MAT, IPA]
    final_input = np.array([[pkn, ind, mat, ipa]])
    
    # B. Prediksi
    try:
        # Normalisasi
        input_scaled = scaler.transform(final_input)
        
        # Hitung Probabilitas
        probs = model.predict_proba(input_scaled)[0]
        classes = model.classes_
        
        # Urutkan Top 6
        sorted_indices = np.argsort(probs)[::-1]
        
        # C. Tampilkan Hasil
        st.success("✅ Analisis Selesai! Berikut rekomendasi sekolah untukmu:")
        
        st.markdown("### 🏫 Top 6 Sekolah Rekomendasi")
        
        for i in range(6):
            idx = sorted_indices[i]
            school_name = classes[idx]
            probability = probs[idx]
            
            # Logic warna bar
            bar_color = "green" if probability > 0.5 else "orange" if probability > 0.2 else "red"
            
            col_icon, col_text = st.columns([1, 8])
            with col_icon:
                st.markdown(f"<h2 style='text-align: center; color: gray;'>#{i+1}</h2>", unsafe_allow_html=True)
            with col_text:
                st.write(f"**{school_name}**")
                st.progress(int(probability * 100))
                st.caption(f"Tingkat Kecocokan: {probability:.1%}")
            st.markdown("---")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

# ==========================================
# 5. FOOTER
# ==========================================
st.markdown("""
<div class="disclaimer">
    <b>DISCLAIMER:</b><br>
    Hasil rekomendasi bersifat PREDIKSI berdasarkan data historis PPDB 2025. 
    Tidak menjamin kelulusan 100%. Gunakan sebagai referensi.
    <br><br>
    Developed with ❤️ by Kelompok 3
</div>
""", unsafe_allow_html=True)