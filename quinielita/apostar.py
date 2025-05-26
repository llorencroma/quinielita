import streamlit as st
from models.db import get_connection
from utils.security import validate_phone, validate_name, validate_pin
import json

def main():
    st.title("🎯 Realizar Apuesta")

    conn, cur = get_connection(), None
    cur = conn.cursor()

    # ---------- 1 · selector de temas ----------
    temas = cur.execute("SELECT id, nombre, bote_total FROM temas").fetchall()
    if not temas:
        st.warning("No hay temas disponibles todavía."); return

    opciones = {f"{n} (Bote {b:.2f} €)": i for i, n, b in temas}
    tema_lbl = st.selectbox("Selecciona un tema", ["— selecciona —"] + list(opciones))
    tema_id  = opciones.get(tema_lbl)

    # ---------- 2 · mostrar formulario solo si hay selección válida ----------
    if tema_id:
        nombre_tema, desc, modo = cur.execute(
    "SELECT nombre, descripcion, modo FROM temas WHERE id=?", (tema_id,)
).fetchone()

        st.header(nombre_tema); st.write(desc); st.divider()

        with st.form("form_apuesta"):
            nombre   = "te" #st.text_input("Tu nombre")
            tel      = "656565678" #st.text_input("Teléfono (+34678901234)")
            pin      = st.text_input("PIN (9876)", type="password")
            monto    = 1
            st.write(f"Apuesta fija: 💶 {monto} EUR")

            # --- opciones dinámicas ---
            # ---------- selector según modo ----------
            if modo == "cerrada":
                opciones = [o[0] for o in cur.execute(
                    "SELECT descripcion FROM opciones_apuesta WHERE tema_id=?", (tema_id,)
                )]
                seleccion = st.radio("Selecciona una opción", opciones)

            elif modo == "combinacion":
                opciones = [o[0] for o in cur.execute(
                    "SELECT descripcion FROM opciones_apuesta WHERE tema_id=?", (tema_id,)
                )]
                seleccion = st.multiselect("Selecciona una o varias opciones",
                                        opciones, max_selections=len(opciones))

            else:  # abierta
                txt = st.text_input("Escribe tu respuesta")
                seleccion = [txt] if txt else []

            enviar = st.form_submit_button("Confirmar apuesta")

         # ---------- FIN FORMULARIO----------

        # ---------- 3 · procesa envío ----------
        if enviar:
            if not (validate_name(nombre) and validate_phone(tel) and validate_pin(pin)):
                st.error("Datos inválidos. Revisa nombre, teléfono o PIN."); return
            if not seleccion:
                st.error("Debes elegir al menos una opción."); return

            detalle = json.dumps(seleccion if isinstance(seleccion, list)
                                 else [seleccion])

            cur.execute(
                "INSERT INTO apuestas (tema_id,nombre,telefono,pin,detalle_apuesta,monto)"
                " VALUES (?,?,?,?,?,?)",
                (tema_id, nombre, tel, pin, detalle, monto)
            )
            conn.commit()

            st.session_state.apuesta_ok = True
            st.session_state.active_page = "Inicio"   # regresa a inicio
            st.rerun()

    # ---------- 4 · confirma tras el rerun ----------
    if st.session_state.get("apuesta_ok"):
        st.success("✅ Apuesta registrada correctamente.")
        st.info("🕒 Se validará manualmente tras recibir el pago.")
        del st.session_state["apuesta_ok"]
