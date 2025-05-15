import streamlit as st
import pandas as pd
import json
from models.db import get_connection
from utils.security import authenticate_admin

# --------------- utilidades ----------------------------------
def is_mesa(titulo: str) -> bool:
    """Devuelve True si el tema es el juego de la mesa."""
    return titulo.lower().startswith("¿quién estará en la mesa")

# -------------------------------------------------------------
def main():
    st.title("🔧 Panel de Administración")

    # ---------- login ----------------------------------------
    if not st.session_state.get("admin_ok"):
        pwd = st.text_input("Contraseña admin", type="password")
        if st.button("Entrar"):
            if authenticate_admin(pwd):
                st.session_state.admin_ok = True
                st.success("Acceso concedido"); st.rerun()
            else:
                st.error("Contraseña incorrecta")
        return

    # ---------- conexión DB ----------------------------------
    conn = get_connection()
    cur  = conn.cursor()

    # ---------- métricas -------------------------------------
    total, pend, val = cur.execute("""
        SELECT COUNT(*),
               SUM(CASE estado WHEN 'no validado' THEN 1 ELSE 0 END),
               SUM(CASE estado WHEN 'validado'    THEN 1 ELSE 0 END)
        FROM apuestas
    """).fetchone()

    bote_total = cur.execute("SELECT COALESCE(SUM(bote_total),0) FROM temas").fetchone()[0]
    temas_act  = cur.execute("SELECT COUNT(*) FROM temas").fetchone()[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Apuestas totales", total)
    c2.metric("Pendientes",       pend)
    c3.metric("Validadas",        val)
    c4.metric("Bote total (€)",   f"{bote_total:.2f}")
    st.info(f"Temas activos: {temas_act}")
    st.divider()

    # ---------- pendientes -----------------------------------
    st.header("📝 Apuestas pendientes de validación")
    pend_rows = cur.execute("""
        SELECT a.id, t.id, t.nombre, a.nombre,
            a.telefono,                     -- ← teléfono
            a.detalle_apuesta, a.fecha
        FROM apuestas a
        JOIN temas t ON a.tema_id = t.id
        WHERE a.estado = 'no validado'
        ORDER BY a.fecha
    """).fetchall()

    if pend_rows:
        df_pend = pd.DataFrame(
            [
                (r[0], r[2], r[3], r[4],                 # teléfono = r[4]
                ", ".join(json.loads(r[5])), r[6])      # detalle y fecha
                for r in pend_rows
            ],
            columns=["ID", "Tema", "Jugador", "Teléfono", "Selección", "Fecha"]
        )
        st.dataframe(df_pend, use_container_width=True, height=250)

        for ap_id, tema_id, tema_nom, jug, tel, det_json, fecha in pend_rows:
            with st.expander(f"#{ap_id} – {jug} ({tema_nom})"):
                selec = ", ".join(json.loads(det_json))
                st.write(f"**Teléfono:** {tel}")
                st.write(f"**Selección:** {selec}")
                st.write(f"**Fecha:** {fecha}")
                if st.button(f"✅ Validar {ap_id}", key=f"val_{ap_id}"):
                    validar_apuesta(cur, ap_id, tema_id, tema_nom, det_json)
                    conn.commit()
                    st.success(f"Apuesta {ap_id} validada.")
                    st.rerun()
    else:
        st.success("No hay apuestas pendientes.")

    # ---------- validadas ------------------------------------
    st.header("✅ Apuestas validadas (posible anulación)")
    val_rows = cur.execute("""
        SELECT a.id, t.id, t.nombre, a.nombre,
            a.telefono,                     -- ← teléfono
            a.detalle_apuesta, a.fecha
        FROM apuestas a
        JOIN temas t ON a.tema_id = t.id
        WHERE a.estado = 'validado'
        ORDER BY a.fecha DESC
    """).fetchall()

    if val_rows:
        df_val = pd.DataFrame(
            [
                (r[0], r[2], r[3], r[4],                 # teléfono
                ", ".join(json.loads(r[5])), r[6])
                for r in val_rows
            ],
            columns=["ID", "Tema", "Jugador", "Teléfono", "Selección", "Fecha"]
        )
        st.dataframe(df_val, use_container_width=True, height=250)

        for ap_id, tema_id, tema_nom, jug, tel, det_json, fecha in val_rows:
            with st.expander(f"#{ap_id} – {jug} ({tema_nom})"):
                selec = ", ".join(json.loads(det_json))
                st.write(f"**Teléfono:** {tel}")
                st.write(f"**Selección:** {selec}")
                st.write(f"**Fecha:** {fecha}")
                if st.button(f"❌ Invalidar {ap_id}", key=f"inv_{ap_id}"):
                    invalidar_apuesta(cur, ap_id, tema_id, tema_nom, det_json)
                    conn.commit()
                    st.warning(f"Apuesta {ap_id} anulada.")
                    st.rerun()
    else:
        st.info("No hay apuestas validadas todavía.")

    
    # 📇 Agenda de jugadores – nombre, teléfono y nº de apuestas
# ------------------------------------------------------------
    st.header("📇 Agenda de jugadores")

    agenda_rows = cur.execute("""
        SELECT  nombre,
                telefono,
                COUNT(*)  AS total_apuestas,
                SUM(CASE estado WHEN 'validado' THEN 1 ELSE 0 END) AS validadas
        FROM apuestas
        GROUP BY nombre, telefono
        ORDER BY nombre COLLATE NOCASE
    """).fetchall()

    if agenda_rows:
        df_agenda = pd.DataFrame(
            agenda_rows,
            columns=["Jugador", "Teléfono", "Apuestas totales", "Validadas"]
        )
        st.dataframe(df_agenda, use_container_width=True, height=300)
    else:
        st.info("De momento nadie ha apostado.")

    # --- alta de temas --------------------------------------------
    st.header("➕ Crear un nuevo tema")

    with st.form("add_tema"):
        nombre = st.text_input("Nombre del tema")
        desc   = st.text_area("Descripción")
        opciones_raw = st.text_input("Opciones separadas por coma "
                                    "(deje vacío si será respuesta libre)")

        modo = st.selectbox(
            "Modalidad de respuesta",
            ["cerrada (una opción)",
            "combinacion (multi-selección de opciones)",
            "abierta (texto libre)"]
        )

        submit = st.form_submit_button("Crear tema")

    if submit and nombre.strip():
        modo_val = modo.split()[0]          # 'cerrada' | 'combinacion' | 'abierta'
        cur.execute(
            "INSERT INTO temas (nombre, descripcion, bote_total, modo) "
            "VALUES (?,?,0,?)",
            (nombre.strip(), desc.strip(), modo_val)
        )
        tema_id = cur.lastrowid

        if modo_val != "abierta":           # sólo si hay lista cerrada
            for op in [o.strip() for o in opciones_raw.split(",") if o.strip()]:
                cur.execute(
                    "INSERT INTO opciones_apuesta (tema_id, descripcion, monto_total) "
                    "VALUES (?,?,0)", (tema_id, op)
                )
        conn.commit(); st.success("Tema creado."); st.rerun()



# ------------------------------------------------------------
# 🗑️  Gestión de temas  –  eliminar tema por completo
# ------------------------------------------------------------
    st.header("🗑️ Eliminar un tema")

    temas_rows = cur.execute("""
        SELECT id, nombre, bote_total,
            (SELECT COUNT(*) FROM apuestas WHERE tema_id=t.id) AS n_apuestas
        FROM temas t
        ORDER BY id
    """).fetchall()

    if temas_rows:
        for tema_id, tema_nom, bote_t, n_ap in temas_rows:
            exp_key = f"deltema_{tema_id}"
            with st.expander(f"{tema_nom}  –  bote {bote_t:.2f} €  –  {n_ap} apuestas", expanded=False):
                st.warning(
                    "⚠️ **Acción irreversible**: se borrarán el tema, "
                    "sus opciones y TODAS las apuestas asociadas."
                )
                if st.button(f"❌ Eliminar «{tema_nom}»", key=exp_key):
                    borrar_tema_completo(cur, tema_id)
                    conn.commit()
                    st.success(f"Tema «{tema_nom}» eliminado.")
                    st.rerun()
    else:
        st.info("No hay temas creados.")

# -------------------------------------------------------------
# business logic
# -------------------------------------------------------------
def validar_apuesta(cur, ap_id, tema_id, tema_nom, det_json):
    # 1) estado
    cur.execute("UPDATE apuestas SET estado='validado' WHERE id=?", (ap_id,))
    # 2) bote +1
    cur.execute("UPDATE temas SET bote_total = bote_total + 1 WHERE id=?", (tema_id,))
    # 3) opcional: sumar contador
    if not is_mesa(tema_nom):
        detalle = " | ".join(sorted(json.loads(det_json)))
        cur.execute("""
            INSERT INTO opciones_apuesta (tema_id, descripcion, monto_total)
            VALUES (?, ?, 1)
            ON CONFLICT(tema_id, descripcion)
            DO UPDATE SET monto_total = monto_total + 1
        """, (tema_id, detalle))

def invalidar_apuesta(cur, ap_id, tema_id, tema_nom, det_json):
    # 1) estado
    cur.execute("UPDATE apuestas SET estado='anulado' WHERE id=?", (ap_id,))
    # 2) bote -1 (sin ir a negativo)
    cur.execute("""
        UPDATE temas
        SET bote_total = CASE WHEN bote_total>0 THEN bote_total-1 ELSE 0 END
        WHERE id=?""", (tema_id,))
    # 3) opcional: restar contador
    if not is_mesa(tema_nom):
        detalle = " | ".join(sorted(json.loads(det_json)))
        cur.execute("""
            UPDATE opciones_apuesta
            SET monto_total = CASE
                WHEN monto_total>0 THEN monto_total-1 ELSE 0 END
            WHERE tema_id=? AND descripcion=?""",
            (tema_id, detalle))


def borrar_tema_completo(cur, tema_id: int) -> None:
    """Elimina tema + opciones + apuestas."""
    cur.execute("DELETE FROM apuestas        WHERE tema_id=?", (tema_id,))
    cur.execute("DELETE FROM opciones_apuesta WHERE tema_id=?", (tema_id,))
    cur.execute("DELETE FROM temas           WHERE id=?",      (tema_id,))