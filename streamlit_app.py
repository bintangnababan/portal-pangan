import streamlit as st

st.set_page_config(page_title="Portal Pangan Indonesia", page_icon="🌾", layout="wide")

# Load Global CSS
try:
    with open("assets/css/theme.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

if "role" not in st.session_state:
    st.session_state.role = "Public"

with st.sidebar:
    st.markdown("### 🔐 Akses Admin")
    
    if st.session_state.role == "Public":
        # Membungkus login dengan st.form agar bisa merespons tombol Enter
        with st.form(key="login_form"):
            password = st.text_input("Password", type="password")
            # st.form_submit_button otomatis terpicu jika user menekan Enter di text_input
            submit_login = st.form_submit_button("Login")
            
            if submit_login:
                if password == "admin123":
                    st.session_state.role = "Admin"
                    st.rerun()
                else:
                    st.error("Password Salah!")
    else:
        st.write(f"Logged in as: **{st.session_state.role}**")
        # Form terpisah untuk logout
        with st.form(key="logout_form"):
            submit_logout = st.form_submit_button("Logout")
            if submit_logout:
                st.session_state.role = "Public"
                st.rerun()

import runpy

# Definisi Navigasi Clean Architecture
pages = {
    "Analisis Publik": [
        ("Executive Dashboard", "views/dashboard.py"),
        ("Regional Map", "views/regional_map.py"),
        ("Predictive AI", "views/forecasting.py"), # Segera kita lengkapi
    ],
}

if st.session_state.role == "Admin":
    pages["Manajemen Data"] = [
        ("Data Ingestion", "views/upload_data.py"),
        ("Pipeline Engine", "views/admin_pipeline.py"),
    ]

menu_category = st.sidebar.radio("Pilih Menu", list(pages.keys()))
menu_items = pages[menu_category]
selected_item = st.sidebar.radio(
    "Pilih Halaman",
    menu_items,
    format_func=lambda item: item[0],
)

runpy.run_path(selected_item[1], run_name="__main__")
