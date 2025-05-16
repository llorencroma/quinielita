import streamlit as st
from models.db import get_connection
import pandas as pd
import json

def main():
    st.title("📜 Todas las Apuestas")

    conn = get_connection()
    cursor = conn.cursor()

    st.subheader("🔍 Buscar tus apuestas")

    search_term = st.text_input("Introduce tu nombre para buscar tus apuestas:")

    query = '''
        SELECT a.fecha, t.nombre as tema, a.nombre as jugador, a.detalle_apuesta, a.monto, a.estado
        FROM apuestas a
        JOIN temas t ON a.tema_id = t.id
        ORDER BY a.fecha DESC
    '''
    apuestas = cursor.execute(query).fetchall()

    if not apuestas:
        st.info("Todavía no hay apuestas registradas.")
        return

    df = pd.DataFrame(apuestas, columns=["Fecha", "Tema", "Jugador", "Detalle", "Monto (€)", "Estado"])

    df["Detalle"] = df["Detalle"].apply(lambda x: ", ".join(json.loads(x)))

    if search_term:
        df = df[df["Jugador"].str.contains(search_term, case=False, na=False)]

    def formato_estado(estado):
        if estado == "validado":
            return "🟢 Validado"
        elif estado =="anulado":
            return "❌ Anulada"
        else:
            return "⚪ Pendiente"

    df["Estado"] = df["Estado"].apply(formato_estado)

    st.dataframe(df, use_container_width=True)
