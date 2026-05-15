import sys
import os
# Menambahkan folder root (utama) ke dalam sistem pembacaan Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from database.queries import fetch_historical_data
from forecasting.run_pipeline import execute_forecasting_pipeline

st.markdown('<h1 class="main-header">🧠 ML Pipeline Engine</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Pusat kendali (Orchestrator) untuk melatih ulang model Facebook Prophet.</p>', unsafe_allow_html=True)

df = fetch_historical_data()

if df.empty:
    st.warning("⚠️ Data harga historis masih kosong. Lakukan Data Ingestion terlebih dahulu.")
    st.stop()

# Agregasi untuk menghitung jumlah komoditas
komoditas_list = df['nama_komoditas'].unique()
st.info(f"📊 Terdeteksi **{len(komoditas_list)} komoditas** siap untuk dianalisis.")

col1, col2 = st.columns(2)
with col1:
    pred_days = st.number_input("Target Hari Prediksi", min_value=7, max_value=90, value=30, step=1)
with col2:
    st.write("Mulai proses *Machine Learning*.")
    mulai = st.button("🚀 Jalankan Pipeline", type="primary", use_container_width=True)

if mulai:
    my_bar = st.progress(0)
    status_text = st.empty()
    
    # Fungsi pembantu untuk mengupdate loading bar dari dalam pipeline
    def update_ui(current_step, total_steps, nama_komoditas):
        progress = current_step / total_steps
        my_bar.progress(progress)
        status_text.text(f"Sedang melatih model untuk: {nama_komoditas}...")

    # Memanggil engine utama
    berhasil = execute_forecasting_pipeline(df, pred_days, progress_callback=update_ui)
    
    # Selesai
    my_bar.progress(1.0)
    status_text.text("✅ Pipeline Selesai!")
    st.cache_data.clear() # Bersihkan cache prediksi lama
    st.success(f"🎉 Selesai! Berhasil memprediksi {berhasil} komoditas.")
    st.balloons()