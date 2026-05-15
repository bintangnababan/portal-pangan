import streamlit as st
import pandas as pd
from database.client import get_db

st.markdown('<h1 class="main-header">⚙️ Data Ingestion System</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Modul admin untuk memperbarui database Supabase via Excel/CSV.</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Pilih file data referensi harga", type=['csv', 'xlsx'])

if uploaded_file is not None:
    with st.spinner("Membaca file..."):
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    
    st.markdown("#### Preview Data")
    st.dataframe(df.head(), use_container_width=True)

    if st.button("🚀 Sinkronisasi ke Database", type="primary"):
        with st.spinner("Sedang memproses dan menyimpan data..."):
            try:
                # Standardisasi Kolom
                df = df.rename(columns={
                    'Tanggal': 'tanggal', 'Nama Komoditas': 'nama_komoditas',
                    'Nama Pasar': 'nama_pasar', 'Jenis Pasar': 'jenis_pasar',
                    'Harga': 'harga', 'Desa/Kelurahan': 'desa_kelurahan',
                    'Kecamatan': 'kecamatan', 'Kabupaten/Kota': 'kabupaten_kota',
                    'Provinsi': 'provinsi', 'Pulau': 'pulau', 'Zona': 'zona'
                })

                df['tanggal'] = pd.to_datetime(df['tanggal']).dt.strftime('%Y-%m-%d')
                records = df.to_dict(orient='records')

                # Chunking Insert (500 baris per batch agar tidak timeout)
                chunk_size = 500
                progress_bar = st.progress(0)
                db = get_db()
                
                for i in range(0, len(records), chunk_size):
                    chunk = records[i:i + chunk_size]
                    db.table("harga_pangan").insert(chunk).execute()
                    progress_bar.progress(min((i + chunk_size) / len(records), 1.0))

                # Hapus cache agar Dashboard langsung membaca data baru
                st.cache_data.clear()
                
                st.success(f"✅ Sukses! {len(records)} baris data masuk ke database.")
                st.balloons()
            except Exception as e:
                st.error(f"Gagal memproses data: {e}")