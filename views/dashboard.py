import streamlit as st
from database.queries import fetch_historical_data
from services.analytics_service import get_kpi_metrics
from services.anomaly_service import detect_anomalies, calculate_volatility
from components.charts import render_trend_chart, render_anomaly_scatter
from components.filters import render_sidebar_filters
from components.cards import render_kpi_cards

st.markdown('<h1 class="main-header">📈 Executive Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Pemantauan Harga Pangan Nasional Terkini</p>', unsafe_allow_html=True)

# 1. Fetch Data
df = fetch_historical_data()
if df.empty:
    st.stop()

# 2. Sidebar Filters (Menggunakan Reusable Component)
selected_komoditas, selected_provinsi = render_sidebar_filters(df, include_provinsi=True)

# 3. Filter Dataframe
df_filtered = df[df['nama_komoditas'] == selected_komoditas]
if selected_provinsi != "Nasional":
    df_filtered = df_filtered[df_filtered['provinsi'] == selected_provinsi]

# 4. Main Rendering
if not df_filtered.empty:
    # Agregasi data tren
    df_trend = df_filtered.groupby('tanggal')['harga'].mean().reset_index().sort_values('tanggal')
    
    # --- SECTION 1: KPI CARDS ---
    # Hitung metrik lewat service, lalu render lewat component
    terakhir, tertinggi, terendah, selisih, pct = get_kpi_metrics(df_trend)
    render_kpi_cards(terakhir, tertinggi, terendah, pct, len(df_filtered))

    st.markdown("---")

    # --- SECTION 2: MAIN CHART ---
    st.markdown("### 📊 Tren Pergerakan Harga")
    render_trend_chart(df_trend)

    # --- SECTION 3: ADVANCED ANALYTICS ---
    st.markdown("### 🔍 Advanced Market Intelligence")
    col_a, col_b = st.columns([1, 3])
    
    # Hitung anomali dan volatilitas lewat service
    vol_score = calculate_volatility(df_trend)
    df_anom = detect_anomalies(df_trend)
    anomalies = df_anom[df_anom['is_anomaly'] == 1]

    with col_a:
        st.write("**Market Volatility Index**")
        if vol_score > 5: 
            st.error(f"High: {vol_score:.2f}%")
        else: 
            st.success(f"Low: {vol_score:.2f}%")
            
    with col_b:
        if not anomalies.empty:
            st.warning(f"⚠️ Terdeteksi {len(anomalies)} titik anomali harga.")
            # Render titik anomali lewat component
            render_anomaly_scatter(anomalies)
        else:
            st.success("✅ Tidak ditemukan anomali harga.")

else:
    st.info("💡 Data tidak ditemukan untuk filter yang dipilih.")