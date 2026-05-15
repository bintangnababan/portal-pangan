import pandas as pd
import numpy as np

def detect_anomalies(df, window=7, threshold=2):
    """Mendeteksi anomali menggunakan Z-Score"""
    df = df.copy().sort_values('tanggal')
    df['rolling_mean'] = df['harga'].rolling(window=window).mean()
    df['rolling_std'] = df['harga'].rolling(window=window).std()
    
    df['z_score'] = (df['harga'] - df['rolling_mean']) / df['rolling_std']
    df['is_anomaly'] = df['z_score'].apply(lambda x: 1 if pd.notnull(x) and abs(x) > threshold else 0)
    return df

def calculate_volatility(df):
    """Menghitung indeks volatilitas (simpangan baku persentase perubahan)"""
    if len(df) < 2: return 0
    pct_change = df['harga'].pct_change().dropna()
    return pct_change.std() * 100