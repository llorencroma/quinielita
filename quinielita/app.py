import streamlit as st

# Configurar la página primero
st.set_page_config(
    page_title="ChusBet 365 🎯",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

from models import db
from streamlit_option_menu import option_menu
import tutorial
import inicio
import apostar
import ranking
import apuestas
import admin
import resumen

db.init_db()

st.sidebar.title("Menú")

# Diccionario de páginas
pages = {
    "Inicio": inicio.main,
    #"Resumen": resumen.main,
    "Apostar": apostar.main,
    "Ranking": ranking.main,
    "Todas las Apuestas": apuestas.main,
    "Admin": admin.main,
    "Tutorial": tutorial.main,
}


# ------- navegación y lógica de página -------
with st.sidebar:
    st.image("images/image2.png", width=250)

    page = option_menu(
        "Menú", list(pages.keys()),
        icons=["house", "speedometer", "currency-dollar", "trophy", "list-columns", "gear"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#FF4B4B", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left"},
            "nav-link-selected": {"background-color": "#FF4B4B", "color": "white"},
        }
    )

# ------- render de la página activa -------
pages[page]()
