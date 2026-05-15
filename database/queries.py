import streamlit as st
import pandas as pd
from database.client import get_db

@st.cache_data(ttl=3600, show_spinner="Mengambil data historis...")
def fetch_historical_data():
    try:
        db = get_db()
        response = db.table("harga_pangan").select("*").execute()
        df = pd.DataFrame(response.data)
        if not df.empty:
            df['tanggal'] = pd.to_datetime(df['tanggal'])
            df['harga'] = pd.to_numeric(df['harga'])
        return df
    except RuntimeError as e:
        st.error(str(e))
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600, show_spinner="Mengambil data prediksi...")
def fetch_forecast_data():
    try:
        db = get_db()
        response = db.table("prediksi_harga").select("*").execute()
        df = pd.DataFrame(response.data)
        if not df.empty:
            df['tanggal'] = pd.to_datetime(df['tanggal'])
        return df
    except RuntimeError as e:
        st.error(str(e))
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()