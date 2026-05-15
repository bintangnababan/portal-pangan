# 🌾 Pangan Analytics Platform | Market Intelligence Dashboard

Sebuah platform intelijen bisnis (*Business Intelligence*) berbasis web untuk memantau, menganalisis, dan memprediksi tren harga komoditas pangan nasional di Indonesia. Dibangun dengan arsitektur modular yang skalabel menggunakan **Streamlit**, **Supabase**, dan **Facebook Prophet AI**.

---

## ✨ Fitur Utama

* **📊 Executive Dashboard:** Pemantauan harga terkini secara *real-time* dengan metrik KPI dinamis, visualisasi tren historis, dan analitik data mentah.
* **🗺️ Regional Spatial Map:** Peta *Choropleth* interaktif untuk melihat distribusi harga pangan di berbagai provinsi se-Indonesia (Geospatial Analysis).
* **🔮 Predictive AI (Forecasting):** Prediksi harga komoditas 30 hari ke depan menggunakan model *Time-Series Machine Learning* (Facebook Prophet) dengan *Confidence Interval*.
* **🔍 Advanced Market Intelligence:** Deteksi otomatis anomali harga (lonjakan tidak wajar) menggunakan *Z-Score* dan perhitungan Indeks Volatilitas Pasar.
* **🔐 Admin & Ingestion System:** Sistem otorisasi (*Role-Based Access*) untuk Admin melakukan *Upload* data via Excel/CSV dan menjalankan *Training ML Pipeline* secara manual.

---

## 🏗️ Arsitektur Proyek (Modular & Clean Architecture)

Proyek ini menggunakan pemisahan *layer* secara tegas antara UI, Logika Bisnis, dan Akses Database:

```text
PORTAL-PANGAN/
├── .streamlit/
│   └── secrets.toml             # Kredensial Database (Ignored by Git)
├── streamlit_app.py                       # Main Router, Navigation API & Auth
├── requirements.txt             # Dependensi Python
├── assets/
│   └── css/theme.css            # Custom Styling & UI/UX
├── components/                  # Reusable UI Layer (Tanpa logika berat)
│   ├── cards.py                 # Modul KPI Cards
│   ├── charts.py                # Modul Grafik Plotly
│   ├── filters.py               # Modul Sidebar Filter
│   └── maps.py                  # Modul Peta Spasial
├── database/                    # Data Access Layer (DAL)
│   ├── client.py                # Koneksi Supabase
│   └── queries.py               # Centralized Queries & st.cache_data
├── forecasting/                 # Machine Learning Layer
│   ├── prophet_engine.py        # Logika matematis model AI
│   └── run_pipeline.py          # Orchestrator training pipeline
├── services/                    # Business Logic Layer
│   ├── analytics_service.py     # Kalkulasi metrik KPI
│   └── anomaly_service.py       # Algoritma Z-Score & Volatilitas
└── views/                       # Presentation Layer (Halaman Streamlit)
    ├── dashboard.py             # Public: Dashboard Utama
    ├── regional_map.py          # Public: Peta Persebaran
    ├── forecasting.py           # Public: Prediksi Harga
    ├── upload_data.py           # Admin: Data Ingestion
    └── admin_pipeline.py        # Admin: ML Pipeline Runner

```text


🛠️ Tech Stack
Frontend / Framework: Streamlit (v1.32.0+)

Database / Backend: Supabase (PostgreSQL)

Machine Learning: Prophet (Time-Series Forecasting)

Data Processing: Pandas, NumPy

Data Visualization: Plotly Express, Plotly Graph Objects

🚀 Panduan Instalasi & Menjalankan Aplikasi
1. Prasyarat
Pastikan Anda sudah menginstal Python 3.10+. Disarankan menggunakan Virtual Environment.

2. Kloning Repositori
Bash
git clone [https://github.com/username-anda/portal-pangan.git](https://github.com/username-anda/portal-pangan.git)
cd portal-pangan
3. Buat Virtual Environment & Instal Dependensi
Bash
python -m venv venv
source venv/bin/activate  # Untuk Linux/Mac
# venv\Scripts\activate   # Untuk Windows

pip install -r requirements.txt
4. Konfigurasi Kredensial Database (Supabase)
Buat folder .streamlit dan file secrets.toml di dalam root proyek Anda:

Bash
mkdir .streamlit
touch .streamlit/secrets.toml
Isi secrets.toml dengan URL dan API Key dari proyek Supabase Anda:

Ini, TOML
SUPABASE_URL = "https://<id-proyek-anda>.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR..."
5. Jalankan Aplikasi
Bash
streamlit run app.py
Aplikasi akan terbuka secara otomatis di browser pada alamat http://localhost:8501.

🔐 Akses Sistem (Login)
Secara bawaan, pengguna hanya bisa melihat menu Public Intelligence. Untuk mengakses fitur pengolahan data dan pelatihan Machine Learning:

Buka Sidebar di sebelah kiri.

Pada bagian Akses Admin, ketikkan password: admin123

Tekan Enter atau tombol Login.

Menu System Administration akan muncul.