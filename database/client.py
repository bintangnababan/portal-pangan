import os
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


def get_supabase_credentials() -> tuple[str, str]:
    url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError(
            "Supabase credentials are missing. Add SUPABASE_URL and SUPABASE_KEY to Streamlit secrets "
            "or set them as environment variables."
        )
    return url, key


@st.cache_resource
def init_connection() -> "Client":
    url, key = get_supabase_credentials()
    return create_client(url, key)


def get_db() -> "Client":
    return init_connection()