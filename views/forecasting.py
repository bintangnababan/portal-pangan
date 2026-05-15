import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from database.client import get_db

# 1. CUSTOM CSS (Konsisten dengan Dashboard Utama)
def inject_forecast_css():
    st.markdown("""
        <style>
        div[data-testid="metric-container"] {
            background-color: var(--secondary-background-color);
            border: 1px solid rgba(128, 128, 128, 0.2);
            padding: 15px 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }
        .insight-card {
            background-color: rgba(37, 99, 235, 0.1);
            border-left: 5px solid #2563eb;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 700; }
        </style>
    """, unsafe_allow_html=True)

inject_forecast_css()

st.title("🔮 Price Forecasting Intelligence")
st.markdown("Analisis prediktif menggunakan *Facebook Prophet AI* untuk memitigasi risiko fluktuasi harga.")

# 3. DATA FETCHING
@st.cache_data(ttl=3600)
def fetch_all_data():
    try:
        db = get_db()
        # Ambil Historis (30 hari terakhir saja untuk perbandingan)
        hist_resp = db.table("harga_pangan").select("tanggal, nama_komoditas, harga").execute()
        # Ambil Prediksi
        fore_resp = db.table("prediksi_harga").select("*").execute()
        return hist_resp.data, fore_resp.data
    except RuntimeError as e:
        st.error(str(e))
        return [], []
    except Exception as e:
        st.error(f"Database Error: {e}")
        return [], []

# Render halaman hanya setelah semua Streamlit komponen terdefinisi
raw_hist, raw_fore = fetch_all_data()

if not raw_fore:
    st.info("💡 Data prediksi belum tersedia. Admin perlu menjalankan 'Pipeline Engine'.")
    st.stop()

# Prepare Dataframes
df_h = pd.DataFrame(raw_hist)
df_h['tanggal'] = pd.to_datetime(df_h['tanggal'])
df_f = pd.DataFrame(raw_fore)
df_f['tanggal'] = pd.to_datetime(df_f['tanggal'])

# 4. SIDEBAR FILTER
with st.sidebar:
    st.markdown("### 🔮 Parameter Prediksi")
    list_k = df_f['nama_komoditas'].unique().tolist()
    selected_k = st.selectbox("Pilih Komoditas", list_k)
    st.markdown("---")
    st.caption("Model: Prophet Time-Series Analysis")
    st.caption("Confidence Level: 80%")

# Filter data berdasarkan pilihan
df_h_filtered = df_h[df_h['nama_komoditas'] == selected_k].groupby('tanggal')['harga'].mean().reset_index()
df_f_filtered = df_f[df_f['nama_komoditas'] == selected_k].sort_values('tanggal')

# 5. KPI METRICS (PREDICTIVE INSIGHTS)
if not df_f_filtered.empty:
    last_hist_price = df_h_filtered['harga'].iloc[-1]
    last_fore_price = df_f_filtered['yhat'].iloc[-1]
    change = last_fore_price - last_hist_price
    pct_change = (change / last_hist_price) * 100

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Harga Terakhir (Real)", f"Rp {last_hist_price:,.0f}")
    with m2:
        st.metric("Prediksi Akhir Periode", f"Rp {last_fore_price:,.0f}", f"{pct_change:.2f}%", delta_color="inverse")
    with m3:
        st.metric("Batas Atas Estimasi", f"Rp {df_f_filtered['yhat_upper'].max():,.0f}")
    with m4:
        st.metric("Batas Bawah Estimasi", f"Rp {df_f_filtered['yhat_lower'].min():,.0f}")

    # 6. CHARTING: HISTORICAL VS FORECAST
    st.markdown("### 📈 Visualisasi Proyeksi Harga")
    
    fig = go.Figure()

    # Confidence Interval Shading
    fig.add_trace(go.Scatter(
        x=df_f_filtered['tanggal'].tolist() + df_f_filtered['tanggal'].tolist()[::-1],
        y=df_f_filtered['yhat_upper'].tolist() + df_f_filtered['yhat_lower'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(37, 99, 235, 0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        name='Confidence Interval'
    ))

    # Historical Line (Solid)
    fig.add_trace(go.Scatter(
        x=df_h_filtered['tanggal'], y=df_h_filtered['harga'],
        name='Data Historis (Real)',
        line=dict(color='#64748b', width=2)
    ))

    # Forecast Line (Dashed)
    fig.add_trace(go.Scatter(
        x=df_f_filtered['tanggal'], y=df_f_filtered['yhat'],
        name='Proyeksi AI',
        line=dict(color='#2563eb', width=4, dash='dash')
    ))

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, linecolor='rgba(128,128,128,0.2)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.1)', title="Harga (Rp)")
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 7. AUTOMATED INSIGHT
    trend_msg = "KENAIKAN" if pct_change > 0 else "PENURUNAN"
    severity = "Waspada" if abs(pct_change) > 5 else "Stabil"
    
    st.markdown(f"""
        <div class="insight-card">
            <h4>💡 Narasi Analitik AI</h4>
            Berdasarkan pola musiman dan tren historis, komoditas <b>{selected_k}</b> diprediksi akan mengalami 
            <b>{trend_msg}</b> sebesar <b>{abs(pct_change):.2f}%</b> dalam 30 hari ke depan. 
            Kondisi ini dikategorikan sebagai <b>{severity}</b>. Disarankan untuk memantau rantai pasokan di wilayah terkait.
        </div>
    """, unsafe_allow_html=True)

    # 8. TABLE DATA
    with st.expander("Lihat Detail Tabel Prediksi Harian"):
        df_table = df_f_filtered[['tanggal', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
        df_table.columns = ['Tanggal', 'Prediksi (Rp)', 'Bawah (Rp)', 'Atas (Rp)']
        st.dataframe(df_table.style.format({
            'Prediksi (Rp)': '{:,.0f}',
            'Bawah (Rp)': '{:,.0f}',
            'Atas (Rp)': '{:,.0f}'
        }), use_container_width=True)

else:
    st.info("Data tidak ditemukan untuk filter ini.")