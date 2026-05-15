import streamlit as st
from database.queries import fetch_historical_data
from components.maps import render_regional_map

st.markdown('<h1 class="main-header">🗺️ Peta Spasial Regional</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Distribusi Tingkat Harga Komoditas se-Indonesia</p>', unsafe_allow_html=True)

df = fetch_historical_data()
if df.empty:
    st.stop()

selected_komoditas = st.selectbox("Pilih Komoditas untuk Dipetakan:", df['nama_komoditas'].unique())

# Logic: Ambil harga rata-rata provinsi HANYA untuk tanggal terakhir
tanggal_terakhir = df['tanggal'].max()
df_terkini = df[(df['nama_komoditas'] == selected_komoditas) & (df['tanggal'] == tanggal_terakhir)]
df_provinsi = df_terkini.groupby('provinsi')['harga'].mean().reset_index()

st.markdown(f"**Peta Panas (Heatmap) Harga per {tanggal_terakhir.strftime('%d %B %Y')}**")
render_regional_map(df_provinsi)