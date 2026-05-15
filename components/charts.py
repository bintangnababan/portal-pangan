import plotly.express as px
import streamlit as st

def render_trend_chart(df_trend):
    """Merender grafik garis utama yang elegan"""
    fig = px.line(df_trend, x='tanggal', y='harga', color_discrete_sequence=["#2563eb"])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=10, b=0), hovermode="x unified",
        xaxis=dict(title="", showgrid=False, linecolor='rgba(128,128,128,0.3)'),
        yaxis=dict(title="Harga (Rupiah)", showgrid=True, gridcolor='rgba(128,128,128,0.1)', zeroline=False)
    )
    fig.update_traces(line=dict(width=3), fill='tozeroy', fillcolor='rgba(37, 99, 235, 0.1)')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def render_anomaly_scatter(df_anomalies):
    """Merender scatter plot untuk titik anomali"""
    fig = px.scatter(df_anomalies, x='tanggal', y='harga', color_discrete_sequence=['#ef4444'])
    fig.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis_title="", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})