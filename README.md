# 🎓 Lolosin.ai - SMP Finder Jakarta Utara

**"Kata AI, bukan katanya."**

**Lolosin.ai** adalah sistem rekomendasi sekolah (SMP Negeri) jalur prestasi akademik di Jakarta Utara. Sistem ini menggunakan algoritma **k-Nearest Neighbors (k-NN)** yang telah divalidasi secara ilmiah untuk mencocokkan profil nilai rapor siswa dengan data historis alumni PPDB tahun 2025.

Proyek ini dibangun dengan arsitektur **Microservices** sederhana, memisahkan logika kecerdasan buatan (Backend) dengan antarmuka pengguna (Frontend).

---

## 🛠️ Teknologi yang Digunakan (Tech Stack)

### Core AI & Data Science

- **Python:** Bahasa pemrograman utama.
- **Scikit-Learn:** Library Machine Learning untuk algoritma k-NN, preprocessing, dan metrik evaluasi.
- **Pandas & NumPy:** Manipulasi dan analisis data numerik.
- **Joblib:** Penyimpanan dan pemuatan model (`.pkl`).

### Backend (API)

- **FastAPI:** Framework modern super cepat untuk membangun API.
- **Uvicorn:** Server ASGI untuk menjalankan FastAPI.
- **Pydantic:** Validasi data input secara ketat.

### Frontend (UI)

- **Streamlit:** Framework untuk membuat web apps data science yang interaktif.
- **Requests:** Library untuk komunikasi HTTP antara Frontend dan Backend.

---

## 📂 Struktur Folder Proyek

Pastikan susunan folder proyek Anda terlihat seperti ini:

```text
Lolosin/
├── DATASET/
│   ├── Data-Cleaning.xlsx       # Data Mentah
│
├── api.py                       # Backend (FastAPI)
├── app.py                       # Frontend (Streamlit)
├── training.py                  # Script Pelatihan Model
├── dashboard.py                 # Script Evaluasi/Laporan Skripsi
├── requirements.txt             # Daftar Library
└── README.md                    # Dokumentasi ini

```

---

## 🚀 Panduan Instalasi (Installation Guide)

Ikuti langkah-langkah ini untuk menjalankan proyek di laptop Anda.

### 1. Prasyarat

Pastikan Anda sudah menginstall **Python** (versi 3.9 ke atas disarankan). Cek dengan perintah:

```bash
python --version

```

### 2. Clone / Siapkan Folder

Masuk ke terminal (Command Prompt / PowerShell / VS Code Terminal) di folder proyek ini.

### 3. Buat Virtual Environment (Opsional tapi Sangat Disarankan)

Supaya library tidak bentrok dengan proyek lain.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

```

### 4. Install Dependencies

Buat file bernama `requirements.txt` lalu isi dengan daftar library di bawah, atau jalankan perintah instalasi manual.

**Isi file `requirements.txt`:**

```text
pandas
numpy
scikit-learn
matplotlib
seaborn
joblib
openpyxl
fastapi
uvicorn
pydantic
streamlit
requests

```

**Jalankan perintah install:**

```bash
pip install -r requirements.txt

```

_(Atau install manual: `pip install pandas numpy scikit-learn matplotlib seaborn joblib openpyxl fastapi uvicorn pydantic streamlit requests`)_

---

## 🏃‍♂️ Cara Menjalankan Aplikasi (How to Run)

Aplikasi ini terdiri dari 3 tahap: **Training**, **Backend**, dan **Frontend**.

### Tahap 1: Melatih Model (Wajib dilakukan pertama kali)

Sebelum aplikasi bisa berjalan, kita harus membuat "Otak AI" (`.pkl`) dari data mentah.
Jalankan perintah:

```bash
python training.py

```

**Hasil:** Jika berhasil, akan muncul file `model_knn_smp.pkl` dan `scaler_smp.pkl` di folder proyek.

### Tahap 2: Menjalankan Backend (Otak)

Buka terminal baru, lalu nyalakan server API. Biarkan terminal ini tetap terbuka.

```bash
uvicorn api:app --reload

```

- Tunggu sampai muncul tulisan: `Application startup complete.`
- API berjalan di: `http://127.0.0.1:8000`

### Tahap 3: Menjalankan Frontend (Wajah)

Buka **Terminal Baru (Terminal Kedua)**, lalu jalankan antarmuka pengguna.

```bash
streamlit run app.py

```

- Browser akan otomatis terbuka dan menampilkan aplikasi Lolosin.ai.

---

## 📊 Evaluasi Model

Jika ingin melihat grafik akurasi dan laporan validasi model, jalankan:

```bash
python dashboard.py

```

**Output:** Akan menghasilkan file gambar `Dashboard_Final_Jujur.png` dan excel laporan.

---

## ⚠️ Disclaimer

Sistem ini dikembangkan sebagai purwarupa (prototype) tugas akhir mata kuliah **Kecerdasan Buatan**. Hasil rekomendasi bersifat prediksi probabilistik berdasarkan data historis dan **tidak menjamin** penerimaan siswa di sekolah terkait. Gunakan sebagai alat bantu pengambilan keputusan, bukan penentu mutlak.

---

**Developed with ❤️ by Kelompok 3**
