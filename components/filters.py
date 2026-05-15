import streamlit as st

def render_sidebar_filters(df, include_provinsi=True):
    """
    Menampilkan sidebar filter dan mengembalikan pilihan user.
    include_provinsi=False digunakan untuk halaman yang tidak butuh filter provinsi.
    """
    with st.sidebar:
        st.markdown("### 🎛️ Parameter Analitik")
        st.markdown("Sesuaikan rentang data yang dianalisis.")
        
        komoditas_list = df['nama_komoditas'].unique().tolist()
        selected_komoditas = st.selectbox("📌 Komoditas", komoditas_list)

        selected_provinsi = "Nasional"
        if include_provinsi:
            provinsi_list = ["Nasional"] + df['provinsi'].dropna().unique().tolist()
            selected_provinsi = st.selectbox("📍 Wilayah", provinsi_list)
        
        st.markdown("---")
        st.caption("Pusat Intelijen Harga Pangan")
        
        return selected_komoditas, selected_provinsi