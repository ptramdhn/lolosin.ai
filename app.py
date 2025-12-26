import streamlit as st
import pandas as pd
import requests

# ==========================================
# 1. KONFIGURASI GLOBAL
# ==========================================
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Lolosin.ai - SMPN Jakarta Utara",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
<style>
    .stNumberInput {margin-bottom: 12px;}
    .main-header {font-size: 2.5rem; font-weight: 700; color: #1E88E5; margin-bottom: 0;}
    .tagline {font-size: 1.2rem; font-style: italic; color: #555; margin-bottom: 20px;}
    .info-box {background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #1E88E5; margin-bottom: 25px;}
    .disclaimer {font-size: 0.9rem; color: #666; text-align: center; margin-top: 30px; border-top: 1px solid #eee; padding-top: 15px;}
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FUNGSI UTILITAS (FRONTEND HELPER)
# ==========================================
def check_api_status():
    """Mengecek apakah server backend hidup"""
    try:
        response = requests.get(f"{API_URL}/", timeout=2)
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        return False
    return False

def input_group(semester_label, key_suffix):
    """Membuat 4 kotak input mapel sekaligus"""
    c1, c2 = st.columns(2)
    with c1:
        # Default value dibuat sedikit variatif biar ga ngetik dari 0
        pkn = st.number_input(f"PKN ({semester_label})", 70.0, 100.0, 88.0, step=0.5, key=f"pkn_{key_suffix}")
        ind = st.number_input(f"B.Ind ({semester_label})", 70.0, 100.0, 88.0, step=0.5, key=f"ind_{key_suffix}")
    with c2:
        mat = st.number_input(f"MTK ({semester_label})", 70.0, 100.0, 85.0, step=0.5, key=f"mat_{key_suffix}")
        ipa = st.number_input(f"IPA ({semester_label})", 70.0, 100.0, 86.0, step=0.5, key=f"ipa_{key_suffix}")
    return pkn, ind, mat, ipa

# ==========================================
# 3. HEADER & INFORMASI
# ==========================================
st.markdown('<p class="main-header">🎓 Lolosin.ai</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">SMPN Jakarta Utara: kata AI, bukan katanya.</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>📋 Petunjuk Pengisian:</strong><br>
    Masukkan nilai rapor (skala 0-100) untuk mata pelajaran <b>PKN, Bahasa Indonesia, Matematika, dan IPA</b>. 
    Data yang dibutuhkan mulai dari <b>Kelas IV Semester 1 sampai dengan Kelas VI Semester 1</b> (Total 5 Semester).
</div>
""", unsafe_allow_html=True)

# Cek status API di awal
api_alive = check_api_status()
if not api_alive:
    st.error("⚠️ **Peringatan Sistem:** Server Otak AI (Backend API) tidak terdeteksi. Aplikasi tidak dapat melakukan prediksi. Mohon jalankan `api.py` terlebih dahulu.")
    # disable tombol kalau API mati

# ==========================================
# 4. FORM INPUT NILAI (TABS)
# ==========================================
tab4, tab5, tab6 = st.tabs(["📘 Kelas 4", "📗 Kelas 5", "📙 Kelas 6"])

# Wadah untuk menampung semua input
scores_data = {'pkn': [], 'ind': [], 'mat': [], 'ipa': []}

with tab4:
    st.markdown("**Semester 1**")
    n1 = input_group("Kls 4 Smt 1", "41")
    st.markdown("---")
    st.markdown("**Semester 2**")
    n2 = input_group("Kls 4 Smt 2", "42")
    # Simpan ke wadah
    for i, m in enumerate(['pkn', 'ind', 'mat', 'ipa']): scores_data[m].extend([n1[i], n2[i]])

with tab5:
    st.markdown("**Semester 1**")
    n3 = input_group("Kls 5 Smt 1", "51")
    st.markdown("---")
    st.markdown("**Semester 2**")
    n4 = input_group("Kls 5 Smt 2", "52")
    for i, m in enumerate(['pkn', 'ind', 'mat', 'ipa']): scores_data[m].extend([n3[i], n4[i]])

with tab6:
    st.markdown("**Semester 1 (Satu Semester Saja)**")
    n5 = input_group("Kls 6 Smt 1", "61")
    for i, m in enumerate(['pkn', 'ind', 'mat', 'ipa']): scores_data[m].append(n5[i])

st.markdown("---")

# ==========================================
# 5. TOMBOL AKSI & KOMUNIKASI KE API
# ==========================================
# Tombol disable kalau API mati biar user ga bingung error
if st.button("🔍 Analisis & Cari Rekomendasi Sekolah", type="primary", disabled=not api_alive):
    
    with st.spinner("sedang menghubungi 'Otak AI' di server... mohon tunggu..."):
        try:
            # A. Siapkan Paket Data untuk Dikirim ke API
            payload = {
                "pkn_scores": scores_data['pkn'],
                "ind_scores": scores_data['ind'],
                "mat_scores": scores_data['mat'],
                "ipa_scores": scores_data['ipa']
            }
            
            # B. Kirim POST Request ke Endpoint /predict
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
            
            # C. Cek Balasan Server
            if response.status_code == 200:
                result = response.json() # Ubah balasan JSON jadi Dictionary Python
                
                # --- TAMPILKAN HASIL ---
                st.success("✅ Analisis Selesai! Berikut hasilnya:")
                
                # 1. Tampilkan Statistik
                stats = result['statistics']
                with st.expander("📊 Lihat Rangkuman Statistik Nilaimu", expanded=True):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Rerata PKN", f"{stats['avg_pkn']:.2f}")
                    c2.metric("Rerata B.Ind", f"{stats['avg_ind']:.2f}")
                    c3.metric("Rerata MTK", f"{stats['avg_mat']:.2f}")
                    c4.metric("Rerata IPA", f"{stats['avg_ipa']:.2f}")
                    st.divider()
                    c5, c6 = st.columns(2)
                    c5.metric("Konsistensi (Std Dev)", f"{stats['consistency_std']:.2f}", help="Semakin kecil angkanya, semakin stabil nilaimu antar mapel.")
                    c6.metric("Nilai Rerata Terendah", f"{stats['min_score']:.2f}")
                
                # 2. Tampilkan Rekomendasi
                st.markdown("### 🏫 Top 6 Sekolah Rekomendasi")
                st.caption("Diurutkan berdasarkan tingkat kecocokan dengan profil alumni tahun 2025.")
                
                for i, rec in enumerate(result['recommendations']):
                    prob = rec['probability']
                    
                    # Visualisasi Progress Bar
                    col_icon, col_text = st.columns([1, 8])
                    with col_icon:
                        st.markdown(f"<h2 style='text-align: center; color: #1E88E5;'>#{i+1}</h2>", unsafe_allow_html=True)
                    with col_text:
                        st.markdown(f"#### {rec['school_name']}")
                        st.progress(int(prob * 100))
                        st.caption(f"Tingkat Kecocokan: **{prob:.1%}**")
                    st.markdown("---")

            else:
                # Handle jika server menolak
                err_detail = response.json().get('detail', 'Terjadi kesalahan pada server.')
                st.error(f"⚠️ Gagal mendapatkan prediksi. Server merespons: {response.status_code} - {err_detail}")

        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Terjadi kesalahan koneksi ke API: {e}")
        except Exception as e:
            st.error(f"⚠️ Terjadi kesalahan tak terduga: {e}")

# ==========================================
# 6. FOOTER & DISCLAIMER
# ==========================================
st.markdown("""
<div class="disclaimer">
    <b>DISCLAIMER:</b><br>
    Sistem AI ini dilatih menggunakan <b>Data Historis PPDB Jalur Prestasi Akademik Tahun 2025</b> di Jakarta Utara.
    Hasil rekomendasi yang ditampilkan HANYA bersifat <b>PREDIKSI</b> berdasarkan pola data masa lalu dan <b>TIDAK MENJAMIN</b> 
    kelulusan atau penerimaan di sekolah yang bersangkutan 100% benar atau valid. 
    Gunakan hasil ini sebagai referensi pendukung, bukan penentu utama keputusan.
    <br><br>
    Developed with ❤️ by Kelompok 3 | Powered by Validated k-NN Algorithm
</div>
""", unsafe_allow_html=True)