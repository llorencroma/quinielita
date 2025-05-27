import streamlit as st
from models.db import get_connection
import pandas as pd, random, json

# paleta de fondos suaves
BG_COLORS = ["#FFF5E5", "#E8F8F8", "#FFEFF3", "#F2F5FF", "#E9F7EF"]

def main():
    st.title("🏆 Ganadores")

    conn = get_connection()
    cur = conn.cursor()
    # 1) Cargamos todos los temas con su respuesta correcta y su bote
    temas = cur.execute(
        "SELECT id, nombre, correct_answer, bote_total, modo FROM temas ORDER BY id"
    ).fetchall()

    # 2) Cargamos todas las apuestas
    apuestas = cur.execute(
        "SELECT nombre AS jugador, tema_id, detalle_apuesta FROM apuestas"
    ).fetchall()

    # 3) Para cada tema, filtramos apuestas acertadas
    #    y agrupamos en un dict: { tema_id: {'ganadores': [...], 'bote': int} }
    resultados = {
        tema_id: {'ganadores': [], 'bote': bote}
        for tema_id, _, _, bote, _ in temas
    }
    for jugador, tema_id, detalle_json in apuestas:
        
        # parsear JSON, o usar fallback si no es JSON válido
        try:
            opciones = json.loads(detalle_json)
        except Exception:
            opciones = [detalle_json]

        _, _, correct_json, _, modo = next(t for t in temas if t[0] == tema_id)
        try:
            correct = json.loads(correct_json)
        except Exception:
            correct = [correct_json]
        # encontrar el correct_answer de este tema
        
        if modo == "cerrada":
            if correct in opciones:

                resultados[tema_id]['ganadores'].append(jugador)
        elif modo == "combinacion":
            if set(correct) == set(opciones): 
                resultados[tema_id]['ganadores'].append(jugador)

        else:
            if opciones == correct:
                resultados[tema_id]['ganadores'].append(jugador)

    # 4) Renderizamos todo
    premios = {}

    

    for tema_id, nombre, correct, bote, modo in temas:
        st.subheader(f"Tema #{tema_id}: {nombre}")
        st.caption(f"Respuesta correcta: **{correct}**")
        st.caption(f"Bote total: {bote}")

        ganadores = resultados[tema_id]['ganadores']
        
        if ganadores:
            premio_por_jugador = resultados[tema_id]['bote'] / len(ganadores)
            st.write(f"Premio por jugador: {premio_por_jugador:.2f}")
            for j in sorted(ganadores):
                premios[j] = premios.get(j, 0) + premio_por_jugador
                st.write(f"• **{j}** — Premio: {premio_por_jugador:.2f}")
            print(f" Premios: {premios}")
        else:
            st.write("— No hay ganadores para este tema —")


    st.subheader(f"Premios totales")
    for key in premios:

        st.write(f"• **{key}** — Premio: {premios[key]:.2f}")