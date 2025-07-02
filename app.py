import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculadora de Calorías y TDEE", layout="centered")

st.title("🔥 Calculadora de Calorías y TDEE")

# Datos del usuario
nombre = st.text_input("Nombre:")
edad = st.number_input("Edad", min_value=10, step=1)
sexo = st.radio("Sexo", ["Hombre", "Mujer"])
peso_lb = st.number_input("Peso (libras)", min_value=50.0, step=0.5)
altura_pies = st.number_input("Altura (pies)", min_value=1, step=1)
altura_pulgadas = st.number_input("Altura (pulgadas)", min_value=0, max_value=11, step=1)
nivel_actividad = st.selectbox("Nivel de actividad física", [
    "Sedentario (poco o nada de ejercicio)",
    "Ligero (ejercicio 1-3 días/semana)",
    "Moderado (ejercicio 3-5 días/semana)",
    "Activo (ejercicio 6-7 días/semana)",
    "Muy activo (dos veces al día o trabajo físico)"
])

objetivo = st.selectbox("¿Cuál es tu objetivo?", ["Perder peso", "Mantener peso", "Ganar masa muscular"])

if st.button("Calcular"):

    # Conversión
    peso_kg = peso_lb * 0.4536
    altura_cm = (altura_pies * 12 + altura_pulgadas) * 2.54

    # Fórmula de Harris-Benedict
    if sexo == "Hombre":
        tmb = 10 * peso_kg + 6.25 * altura_cm - 5 * edad + 5
    else:
        tmb = 10 * peso_kg + 6.25 * altura_cm - 5 * edad - 161

    # Factor de actividad
    factores = {
        "Sedentario (poco o nada de ejercicio)": 1.2,
        "Ligero (ejercicio 1-3 días/semana)": 1.375,
        "Moderado (ejercicio 3-5 días/semana)": 1.55,
        "Activo (ejercicio 6-7 días/semana)": 1.725,
        "Muy activo (dos veces al día o trabajo físico)": 1.9
    }

    tdee = tmb * factores[nivel_actividad]

    st.subheader(f"Hola {nombre} 👋")
    st.write(f"Tu TDEE estimado es: **{tdee:.0f} calorías/día**")

    # Recomendaciones
    st.write("### 🔥 Recomendaciones calóricas:")
    st.write(f"- Para **mantener tu peso**: {int(tdee)} kcal/día")
    st.write(f"- Para **perder peso** (~-500 kcal): {int(tdee - 500)} kcal/día")
    st.write(f"- Para **ganar masa muscular** (+300 kcal): {int(tdee + 300)} kcal/día")

    # Proyección de peso
    semanas = list(range(13))
    peso_actual = peso_lb
    proyeccion = []

    if objetivo == "Perder peso":
        tasa = -1  # 1 lb por semana
    elif objetivo == "Ganar masa muscular":
        tasa = 0.5  # 0.5 lb por semana
    else:
        tasa = 0

    for semana in semanas:
        proyeccion.append(peso_actual + semana * tasa)

    # Gráfica
    fig, ax = plt.subplots()
    ax.plot(semanas, proyeccion, marker='o', color='green')
    ax.set_title("📉 Proyección de Peso en 3 Meses")
    ax.set_xlabel("Semanas")
    ax.set_ylabel("Peso (lb)")
    ax.grid(True)

    st.pyplot(fig)

#adicional.

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Proyección de Peso", layout="centered")
st.title("📉 Proyección de Peso por Déficit o Superávit Calórico")

# Datos del usuario
peso_actual = st.number_input("Peso actual (lbs):", min_value=50.0, max_value=500.0, value=180.0, step=1.0)
tdee = st.number_input("TDEE (Calorías necesarias para mantenerte):", min_value=1000, max_value=6000, value=2500)

# Calorías que planeas consumir al día
calorias_diarias = st.slider("¿Cuántas calorías planeas comer al día?", min_value=1000, max_value=6000, value=2000, step=100)

# Proyección
dias = 90
deficit_diario = tdee - calorias_diarias  # puede ser negativo si comes más que tu TDEE
calorias_por_libra = 3500  # 1 lb = 3500 kcal
cambio_peso_total = deficit_diario * dias / calorias_por_libra
peso_estimado = peso_actual + cambio_peso_total

# Generar proyección diaria
dias_array = np.arange(dias + 1)
peso_array = peso_actual + (deficit_diario * dias_array / calorias_por_libra)

# Mostrar resultado
st.markdown(f"""
### 🧮 Resultado estimado:
- Peso actual: **{peso_actual:.1f} lbs**
- TDEE: **{tdee} kcal**
- Calorías consumidas: **{calorias_diarias} kcal/día**
- Cambio estimado en 90 días: **{cambio_peso_total:+.1f} lbs**
- Peso estimado al día 90: **{peso_estimado:.1f} lbs**
""")

# Mostrar gráfica
fig, ax = plt.subplots()
ax.plot(dias_array, peso_array, color="blue", linewidth=2)
ax.set_title("Proyección de Peso en 90 días")
ax.set_xlabel("Días")
ax.set_ylabel("Peso (lbs)")
ax.grid(True)
st.pyplot(fig)
