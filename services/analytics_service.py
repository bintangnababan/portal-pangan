import pandas as pd

def get_kpi_metrics(df_trend):
    """Menghitung metrik utama untuk KPI Cards"""
    if df_trend.empty:
        return 0, 0, 0, 0, 0

    harga_terakhir = df_trend['harga'].iloc[-1]
    harga_tertinggi = df_trend['harga'].max()
    harga_terendah = df_trend['harga'].min()
    
    selisih = 0
    persentase = 0
    if len(df_trend) > 1:
        harga_sebelumnya = df_trend['harga'].iloc[-2]
        selisih = harga_terakhir - harga_sebelumnya
        persentase = (selisih / harga_sebelumnya) * 100
        
    return harga_terakhir, harga_tertinggi, harga_terendah, selisih, persentase