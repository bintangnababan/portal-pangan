import pandas as pd
from prophet import Prophet
import logging

# Mematikan log Prophet yang sering mengotori terminal
logging.getLogger('cmdstanpy').setLevel(logging.WARNING)

def train_and_predict(df, periods=30):
    """
    Melatih model Prophet dan menghasilkan prediksi.
    df input WAJIB memiliki kolom 'ds' (tanggal) dan 'y' (nilai).
    """
    # Konfigurasi model (bisa dituning di sini ke depannya)
    m = Prophet(
        daily_seasonality=False, 
        yearly_seasonality=True, 
        weekly_seasonality=True,
        changepoint_prior_scale=0.05
    )
    
    m.fit(df)
    
    # Membuat dataframe masa depan
    future = m.make_future_dataframe(periods=periods)
    
    # Melakukan prediksi (mengembalikan yhat, yhat_lower, yhat_upper, trend)
    forecast = m.predict(future)
    
    return forecast