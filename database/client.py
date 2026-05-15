import streamlit as st
from typing import TYPE_CHECKING

try:
    from supabase import create_client
    if TYPE_CHECKING:
        from supabase import Client
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "Supabase is not installed. Install the app dependencies with `pip install -r requirements.txt` "
        "and ensure `supabase==2.3.4` is listed in `requirements.txt`."
    ) from exc

@st.cache_resource
def init_connection() -> "Client":
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError(
            "Supabase credentials are missing. Add SUPABASE_URL and SUPABASE_KEY to Streamlit secrets."
        )
    return create_client(url, key)

db = init_connection()