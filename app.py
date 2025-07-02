import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Calculadora de Calorías y TDEE", layout="centered")

st.title("🔥 Calculadora de Calorías, TDEE y Proyección de Peso")

# Entradas del usuario
nombre = st.text_input("¿Cuál es tu nombre?")
edad = st.number_input("Edad", min_value=10, max_value=100, value=25)
genero = st.selectbox("Género", ["Masculino", "Femenino"])
peso = st.number_input("Peso (lbs)", min_value=50.0, max_value=600.0, value=180.0)
estatura = st.number_input("Estatura (cm)", min_value=130, max_value=250, value=175)
nivel = st.selectbox("Nivel de actividad física", [
    "Sedentario", "Ligero", "Moderado", "Activo", "Muy activo"
])
objetivo = st.radio("¿Cuál es tu objetivo?", ["Perder peso", "Mantener peso", "Ganar músculo"])

# Factor de actividad
factores = {
    "Sedentario": 1.2,
    "Ligero": 1.375,
    "Moderado": 1.55,
    "Activo": 1.725,
    "Muy activo": 1.9
}

# Cálculo de TDEE
bmr = 10 * (peso * 0.453592) + 6.25 * estatura - 5 * edad + (5 if genero == "Masculino" else -161)
tdee = bmr * factores[nivel]

st.subheader("🔍 Resultados")

st.markdown(f"**Tu TDEE estimado es:** {tdee:.0f} calorías/día")

# Recomendaciones
perder_peso = tdee - 500
ganar_peso = tdee + 300

st.markdown(f"""
- Para **mantener tu peso**: {tdee:.0f} kcal/día  
- Para **perder peso**: {perder_peso:.0f} kcal/día  
- Para **ganar músculo**: {ganar_peso:.0f} kcal/día
""")

# --- Slider para personalizar calorías ---
calorias_slider = st.slider("Elige tus calorías diarias:", min_value=1200, max_value=4000, value=int(tdee), step=50)

# --- Proyección de peso dinámica ---
dias = np.arange(0, 91)
peso_inicial = peso
cambio_diario = (calorias_slider - tdee) / 3500
peso_proyectado = peso_inicial + cambio_diario * dias

df = pd.DataFrame({
    "Día": dias,
    "Peso proyectado (lbs)": peso_proyectado.round(2)
})

# --- Gráfica interactiva (Plotly) ---
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["Día"],
    y=df["Peso proyectado (lbs)"],
    mode='lines+markers',
    line=dict(color='royalblue', width=3),
    hovertemplate='Día: %{x}<br>Peso: %{y} lbs'
))

fig.update_layout(
    title="📉 Proyección de Peso (90 días)",
    xaxis_title="Día",
    yaxis_title="Peso (lbs)",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=20, r=20, t=40, b=20),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# --- Ingreso del correo y resumen final ---
correo = st.text_input("📧 Ingresa tu correo para el resumen:")

if correo:
    peso_final = round(peso_proyectado[-1], 2)
    resumen = {
        "Correo": [correo],
        "Peso actual (lbs)": [peso],
        "Calorías seleccionadas (kcal)": [calorias_slider],
        "Objetivo": [objetivo],
        "Peso proyectado en 3 meses (lbs)": [peso_final]
    }
    df_resumen = pd.DataFrame(resumen)
    st.subheader("📋 Resumen final:")
    st.dataframe(df_resumen)
