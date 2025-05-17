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

st.sidebar.title("")

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
        "", list(pages.keys()),
        icons=["house", "speedometer", "currency-dollar", "trophy", "list-columns", "gear"],
        default_index=0,
        styles={
        "container": {"padding": "0!important", "color": "white", "background-color": "#0f1117"},
        "icon": {"color": "white", "font-size": "18px"},
        "nav-link": {
            "font-size": "18px",
            "margin": "0px",
            "color": "white",
            "background-color": "#1e1e2f",
        },
        "nav-link-selected": {
            "background-color": "#ff4b4b",
        },
    },
    )
    st.markdown("---")
    st.markdown("© 2025 ChusBet365 | [View source on GitHub](https://github.com/llorencroma/quinielita)",
        unsafe_allow_html=True
    )

# ------- render de la página activa -------
pages[page]()
