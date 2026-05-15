import streamlit as st

def render_kpi_cards(terakhir, tertinggi, terendah, persentase, total_sampel):
    """Merender 4 kolom KPI utama secara modular"""
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric(
            label="Harga Rata-rata Terkini", 
            value=f"Rp {terakhir:,.0f}", 
            delta=f"{persentase:.2f}%", 
            delta_color="inverse"
        )
    with c2:
        st.metric("Harga Puncak (Historis)", f"Rp {tertinggi:,.0f}")
    with c3:
        st.metric("Harga Terendah (Historis)", f"Rp {terendah:,.0f}")
    with c4:
        st.metric("Total Sampel Data", f"{total_sampel:,}")