import streamlit as st
import plotly.express as px
import json
import urllib.request

@st.cache_resource
def load_geojson():
    """Load GeoJSON langsung dari URL atau file lokal"""
    url = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/refs/heads/master/indonesia.geojson"
    try:
        # Kita baca langsung dari URL agar selalu sinkron
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        st.error(f"Gagal memuat peta: {e}")
        return None

def render_regional_map(df_provinsi):
    geojson = load_geojson()
    if not geojson or df_provinsi.empty:
        st.warning("Data geospasial tidak tersedia.")
        return

    # 1. SINKRONISASI NAMA PROVINSI (SUPABASE -> GEOJSON)
    # Sebelah Kiri = Nama di Supabase Anda | Sebelah Kanan = Nama di GeoJSON Superpikar
    mapping_provinsi = {
        "DKI Jakarta": "Jakarta Raya",
        "DI Yogyakarta": "Yogyakarta",
        "Daerah Istimewa Yogyakarta": "Yogyakarta",
        "Nanggroe Aceh Darussalam": "Aceh",
        "Kepulauan Bangka Belitung": "Bangka Belitung",
        "Papua Barat Daya": "Irian Jaya Barat", # Penyesuaian jika GeoJSON menggunakan nama lama
        "Papua Barat": "Irian Jaya Barat"
    }

    # Buat kolom baru khusus untuk peta, replace nama yang tidak cocok, lalu pastikan formatnya Title Case
    df_provinsi['provinsi_map'] = df_provinsi['provinsi'].replace(mapping_provinsi)
    df_provinsi['provinsi_map'] = df_provinsi['provinsi_map'].str.title()

    # 2. RENDER PETA
    fig = px.choropleth_mapbox(
        df_provinsi, 
        geojson=geojson, 
        locations='provinsi_map',        # Kolom hasil mapping
        featureidkey='properties.state', # Key dari file indonesia.geojson superpikar
        color='harga', 
        color_continuous_scale="RdYlGn_r",
        mapbox_style="carto-positron", 
        zoom=3.8, 
        center={"lat": -2.0, "lon": 118.0},
        opacity=0.8, 
        labels={'harga': 'Rata-rata Harga (Rp)', 'provinsi_map': 'Provinsi'},
        hover_name='provinsi'            # Tetap tampilkan nama asli dari Supabase saat di-hover
    )
    
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0}, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        coloraxis_colorbar=dict(title="Rupiah", orientation="h", y=-0.1)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})