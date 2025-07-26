import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="Asesor Vivienda", page_icon="🏠")

# Encabezado visual
st.image("https://cdn-icons-png.flaticon.com/512/814/814513.png", width=80)
st.markdown("## 🏠 Bienvenido al Asesor Virtual de Vivienda")
st.markdown("Consulta tu estado o registra tus datos para obtener tu puntuación 🧠")

# Cargar base de datos si existe
file_path = 'clientes.csv'
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    df = pd.DataFrame()

# Consulta de cliente
id_input = st.text_input("🔍 Ingrese su ID (o deje en blanco si es nuevo):")

if id_input and id_input in df['ID'].astype(str).values:
    st.success("✅ Cliente encontrado:")
    st.dataframe(df[df['ID'].astype(str) == id_input])
else:
    st.warning("⚠️ ID no encontrado. Ingrese sus datos para registrarse:")

    with st.form("formulario"):
        genero = st.selectbox("👤 Género", ["Mujer", "Hombre"])
        estrato = st.number_input("🏘️ Estrato socio económico", min_value=1, max_value=6)
        endeudamiento = st.number_input("💳 Nivel de endeudamiento (0 a 100)", min_value=0, max_value=100)
        tipo_gestion = st.selectbox("📞 Tipo de Gestión", ["Contactado", "No Contactado"])
        tipo_interes = st.selectbox("⏳ Tipo de Interés", ["De 0 a 30 días", "De 31 a 60 días", "De 61 a 90 días", "Más de 91 días"])
        nivel_academico = st.selectbox("🎓 Nivel académico", ["Primaria", "Secundaria", "Técnico", "Tecnólogo", "Profesional", "Especialización", "Maestría", "Doctorado"])
        tipo_contrato = st.selectbox("📄 Tipo de contrato", ["Fijo", "Indefinido", "Obra o labor", "Prestación de servicios"])
        motivo = st.selectbox("🎯 Motivo de compra", ["Para vivir", "Para inversión"])
        ahorro = st.selectbox("💰 Tipo de ahorro", ["No tiene ahorros", "CDT", "Cuenta de ahorro", "Cuenta corriente", "Cesantias", "AFC", "Otros"])
        submitted = st.form_submit_button("Enviar")

    if submitted:
        # Mapear valores
        nuevo_cliente = {
            'ID': df['ID'].max() + 1 if not df.empty else 1,
            'Género': {'Mujer': 1, 'Hombre': 2}[genero],
            'Estrato socio económico': estrato,
            'Endeudamiento': endeudamiento,
            'Tipo de Gestión': {'Contactado': 1, 'No Contactado': 0}[tipo_gestion],
            'Tipo de Interés': {'De 0 a 30 días': 30, 'De 31 a 60 días': 60, 'De 61 a 90 días': 90, 'Más de 91 días': 120}[tipo_interes],
            'Nivel académico': {'Primaria': 1, 'Secundaria': 2, 'Técnico': 3, 'Tecnólogo': 4, 'Profesional': 5, 'Especialización': 6, 'Maestría': 7, 'Doctorado': 8}[nivel_academico],
            'Tipo de contrato': {'Fijo': 1, 'Indefinido': 2, 'Obra o labor': 3, 'Prestación de servicios': 4}[tipo_contrato],
            'Motivo de compra': {'Para vivir': 1, 'Para inversión': 2}[motivo],
            'Tipo de ahorro': {'No tiene ahorros': 0, 'CDT': 1, 'Cuenta de ahorro': 2, 'Cuenta corriente': 3, 'Cesantias': 4, 'AFC': 5, 'Otros': 6}[ahorro]
        }

        # Calcular puntuación (ejemplo)
        puntaje = 100 - int(endeudamiento) + nuevo_cliente['Estrato socio económico'] * 2
        nuevo_cliente['Puntaje Vivienda'] = min(max(puntaje, 0), 100)

        # Guardar nuevo cliente
        df = pd.concat([df, pd.DataFrame([nuevo_cliente])], ignore_index=True)
        df.to_csv(file_path, index=False)

        st.success(f"🎯 Cliente registrado con ID: {nuevo_cliente['ID']}, PUNTAJE: {nuevo_cliente['Puntaje Vivienda']}")
