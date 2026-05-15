import pandas as pd
from forecasting.prophet_engine import train_and_predict
from database.client import db

def execute_forecasting_pipeline(df_historis, pred_days=30, progress_callback=None):
    """
    Menjalankan loop training untuk setiap komoditas dan menyimpan ke Supabase.
    progress_callback digunakan untuk update UI loading bar di Streamlit.
    """
    # Agregasi ke level nasional untuk mempercepat komputasi awal
    df_nasional = df_historis.groupby(['tanggal', 'nama_komoditas'])['harga'].mean().reset_index()
    list_komoditas = df_nasional['nama_komoditas'].unique()
    
    total_komoditas = len(list_komoditas)
    berhasil = 0

    for i, komoditas in enumerate(list_komoditas):
        try:
            # 1. Update UI Loading (Jika callback diberikan)
            if progress_callback:
                progress_callback(i, total_komoditas, komoditas)
                
            # 2. Siapkan data untuk Prophet
            df_k = df_nasional[df_nasional['nama_komoditas'] == komoditas][['tanggal', 'harga']]
            df_k.columns = ['ds', 'y']
            
            if len(df_k) < 10:
                continue # Skip jika data terlalu sedikit
                
            # 3. Panggil Engine ML
            forecast = train_and_predict(df_k, periods=pred_days)
            
            # 4. Potong data yang disimpan (hanya 30 hari ke belakang + masa depan)
            batas_waktu = df_k['ds'].max() - pd.Timedelta(days=30)
            forecast_to_save = forecast[forecast['ds'] >= batas_waktu]
            
            # 5. Format ke dictionary JSON untuk Supabase
            records = []
            for _, row in forecast_to_save.iterrows():
                records.append({
                    "tanggal": row['ds'].strftime('%Y-%m-%d'),
                    "nama_komoditas": komoditas,
                    "provinsi": "Nasional",
                    "yhat": round(row['yhat'], 2),
                    "yhat_lower": round(row['yhat_lower'], 2),
                    "yhat_upper": round(row['yhat_upper'], 2),
                    "trend": round(row['trend'], 2)
                })
            
            # 6. Upsert ke Database
            db.table("prediksi_harga").upsert(records, on_conflict="tanggal,nama_komoditas,provinsi").execute()
            
            berhasil += 1
            
        except Exception as e:
            print(f"Error memproses {komoditas}: {e}")
            continue
            
    return berhasil