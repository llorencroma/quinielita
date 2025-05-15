import streamlit as st
from models.db import get_connection
import pandas as pd

def main():
    st.title("🏆 Ranking de Jugadores")

    conn = get_connection()
    cursor = conn.cursor()

    data = cursor.execute('''
        SELECT nombre, COUNT(*) as num_apuestas, SUM(monto) as total_apostado
        FROM apuestas
        WHERE estado = 'validado'
        GROUP BY nombre
        ORDER BY total_apostado DESC
    ''').fetchall()

    if data:
        df = pd.DataFrame(data, columns=["Jugador", "Apuestas Validadas", "Total Apostado (€)"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Todavía no hay jugadores apostando.")
