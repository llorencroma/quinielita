# 🎯 Quinielita

**Quinielita** es una app de apuestas ligeras para eventos especiales como bodas, cumpleaños y celebraciones.  El objetivo es que las apuestas se paguen a partir del bote generado con todos los participantes y no a partir de una "banca".

---

## 🚀 Instalación

1. Clona o descarga este repositorio.
2. Instala dependencias:

```bash
pip install streamlit
```
3. Crea la carpeta de base de datos:
```
mkdir quinielita/data
```


## 🏃‍♂️ Cómo correr la app
```
cd quinielita
streamlit run app.py
```

Se abrirá en http://localhost:8501.


## 🧱 Estructura

```
quinielita/
├── app.py
├── *.py  ## todas las diferents páginas de la app
├── /data/
├── /images/
├── /models/
├── /scripts/
├── /utils/
└── README.md
```

## 🔒 Seguridad

- Contraseña para acceder al panel de administración.
- Validación de PIN para poder realizar apuestas. El PIN se distribuya a los participantes a través de algún otro canal.

## 🛠️ Funcionalidades

- Ver temas de apuestas y botes correspondientes por cada tema.
- Realizar apuestas. 
- Ranking de jugadores.
- Ver todas las apuestas.
- Administración de validaciones: el administrador valida manualmente las apuestas después de recibir el pago. El pago se debe hacer a través de otro canal (p.e. Bizum, revolut)
- Creación / Eliminación de temas

