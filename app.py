import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 👉 Estilo claro
st.markdown("""
    <style>
        body {
            background-color: white;
            color: black;
        }
        .stApp {
            background-color: white;
        }
    </style>
""", unsafe_allow_html=True)

# 👉 Configuración de la página
st.set_page_config(page_title="Calculadora Calorías y TDEE", layout="centered")
st.title("🧮 Calculadora de Calorías, TDEE y Proyección de Peso")

# 👉 Entradas del usuario
nombre = st.text_input("Nombre:")
edad = st.number_input("Edad", min_value=1, step=1)
sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])
peso_lbs = st.number_input("Peso (lbs)", min_value=50.0, step=1.0)
altura_cm = st.number_input("Altura (cm)", min_value=100.0, step=1.0)
actividad = st.selectbox("Nivel de actividad física", [
    "Sedentario (poco o ningún ejercicio)",
    "Ligero (ejercicio 1-3 días/semana)",
    "Moderado (ejercicio 3-5 días/semana)",
    "Activo (ejercicio 6-7 días/semana)",
    "Muy activo (entrenamientos intensos)"
])
objetivo = st.selectbox("Objetivo", ["Perder peso", "Mantener peso", "Ganar músculo"])

# 👉 Función para calcular TDEE
def calcular_tdee(sexo, peso_lbs, altura_cm, edad, actividad):
    peso_kg = peso_lbs * 0.4536
    altura_m = altura_cm / 100
    if sexo == "Masculino":
        bmr = 10 * peso_kg + 6.25 * altura_cm - 5 * edad + 5
    else:
        bmr = 10 * peso_kg + 6.25 * altura_cm - 5 * edad - 161

    factores = {
        "Sedentario (poco o ningún ejercicio)": 1.2,
        "Ligero (ejercicio 1-3 días/semana)": 1.375,
        "Moderado (ejercicio 3-5 días/semana)": 1.55,
        "Activo (ejercicio 6-7 días/semana)": 1.725,
        "Muy activo (entrenamientos intensos)": 1.9
    }

    return round(bmr * factores[actividad])

# 👉 Cálculo del TDEE
if nombre and peso_lbs and altura_cm:
    tdee = calcular_tdee(sexo, peso_lbs, altura_cm, edad, actividad)
    st.markdown(f"### Hola {nombre}, tu TDEE estimado es: **{tdee} calorías/día**")

    if objetivo == "Perder peso":
        st.info(f"Para perder peso podrías comer entre **{tdee - 500} y {tdee - 250} cal/día**")
    elif objetivo == "Mantener peso":
        st.info(f"Para mantener tu peso deberías comer aproximadamente **{tdee} cal/día**")
    else:
        st.info(f"Para ganar músculo podrías comer entre **{tdee + 250} y {tdee + 500} cal/día**")

    # 👉 Slider dinámico
    calorias_slider = st.slider("Calorías que planeas consumir por día", 1200, 4000, value=tdee, step=50)

    # 👉 Simulación de peso proyectado
    dias = np.arange(0, 91)
    cambio_diario = (calorias_slider - tdee) / 3500
    peso_proyectado = peso_lbs + cambio_diario * dias

    df = pd.DataFrame({
        "Día": dias,
        "Peso proyectado (lbs)": peso_proyectado.round(2)
    })

    st.markdown("### 📊 Tabla de proyección de peso (3 meses)")
    st.dataframe(df, use_container_width=True)

    # 👉 Gráfica
    fig, ax = plt.subplots()
    ax.plot(dias, peso_proyectado, color='blue', linewidth=2)
    ax.set_title("Proyección de Peso en 90 días")
    ax.set_xlabel("Día")
    ax.set_ylabel("Peso (lbs)")
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")
    ax.grid(False)
    st.pyplot(fig)
