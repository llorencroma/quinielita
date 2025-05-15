import streamlit as st

def main():
    st.title("📖 Tutorial rápido – Cómo usar Quinielita")

    st.markdown("""
### 1. Explora los temas  
En **Inicio** verás cada apuesta disponible con su bote y las cuotas actuales.

### 2. Haz tu apuesta  
Ve a **Apostar**, elige un tema, introduce:  
**• Nombre**, 
**• Teléfono válido**,
**• PIN **,  

selecciona la opción y envía.

### 3. Espera validación  
Tu apuesta queda *pendiente*. El administrador la validará manualmente cuando confirme el pago.

### 4. Revisa resultados  
*Ranking* muestra quién ha apostado más, y en **Todas las Apuestas** puedes buscar las tuyas.

---

> **¿Dudas?** Pregunta al organizador o visita la sección *Admin* si eres administrador.
    """)

    st.success("¡Listo! Usa el menú lateral para empezar en **Inicio**.")
