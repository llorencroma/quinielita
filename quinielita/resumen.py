import streamlit as st
from models.db import get_connection
import pandas as pd, random, json

# paleta de fondos suaves
BG_COLORS = ["#FFF5E5", "#E8F8F8", "#FFEFF3", "#F2F5FF", "#E9F7EF"]

def main() -> None:

    conn   = get_connection()
    cursor = conn.cursor()

    # ---------------- Temas disponibles ----------------
    st.subheader("Resumen Apuestas")

    temas = cursor.execute(
        "SELECT id, nombre, descripcion, bote_total, modo FROM temas"
    ).fetchall()
  
    col1, col2 = st.columns(2)
    cols       = [col1, col2]

    for idx, (id_, nombre, descripcion, bote_total, modo) in enumerate(temas):
        bg = random.choice(BG_COLORS)

        # ---------- cuotas -------------------------------------------
        pendientes = cursor.execute("""
            SELECT COUNT(*) FROM apuestas
            WHERE tema_id=? AND estado='no validado'
        """, (id_,)).fetchone()[0]

        bote_potencial = bote_total + pendientes
        cuotas_html = ""

        # --------- cuotas -----------------------------
        if modo in ("combinacion", "abierta"):          # cuota única
            cuotas_html = (
                f"Premio único actual: <b>{bote_total:.2f} €</b>"
                "<br><small>(si varias apuestas aciertan, se reparte el bote)</small>"
            )
        else:
             # --------- construir HTML completo de la tarjeta ---------
            filas = cursor.execute("""
                SELECT descripcion, monto_total
                FROM opciones_apuesta
                WHERE tema_id = ? AND monto_total > 0  
            """, (id_,)).fetchall() 
            if filas:
                for desc, mt in filas:
                    cuota = (bote_total / mt) if mt else 0
                    cuotas_html += (
                        f"<div style='font-size:0.85rem;margin:.2rem 0;'>"
                        f"🔸 <b>{desc}</b>: {mt} apuestas • Premio {cuota:.2f}x"
                        f"</div>"
                    )
            else:
                cuotas_html = "<em>Sin apuestas aún.</em>"

        card_html = f"""
        <div style='background:{bg};padding:1rem;border-radius:14px;
                    box-shadow:0 2px 6px rgba(0,0,0,0.07);margin-bottom:1rem;'>
            <h3 style='margin:0 0 .3rem 0;font-size:1.15rem;'>{nombre}</h3>
            <p style='margin:0 0 .8rem 0;font-size:.9rem;'>{descripcion}</p>
            <div style='font-size:0.9rem;font-weight:600;margin-bottom:.6rem;'>
                💰 Bote: {bote_total:.2f} €
            </div>
            <div style='font-size:0.9rem;font-weight:600;margin-bottom:.6rem;'>
                💸 Bote potencial: {bote_potencial:.2f} € (incluye apuestas sin  validar)
            </div>
            <details style='margin-bottom:.4rem;'>
                <summary style='cursor:pointer;font-weight:600;'>Premios actuales</summary>
                {cuotas_html}
            </details>
        </div>
        """

        with cols[idx % 2]:
            st.markdown(card_html, unsafe_allow_html=True)

    # ---------------- Últimas apuestas ----------------
    st.subheader("📜 Últimas apuestas")

    ult = cursor.execute("""
        SELECT a.fecha, t.nombre, a.nombre, a.estado
        FROM apuestas a
        JOIN temas  t ON a.tema_id = t.id
        ORDER BY a.fecha DESC
        LIMIT 10
    """).fetchall()

    if ult:
        st.dataframe(
            pd.DataFrame(ult, columns=["Fecha", "Tema", "Jugador", "Estado"]),
            height=250, use_container_width=True
        )
    else:
        st.info("Aún no hay apuestas registradas.")
