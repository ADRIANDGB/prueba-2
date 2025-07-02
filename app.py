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

# Slider para modificar calorías
calorias_slider = st.slider("¿Cuántas calorías planeas consumir al día?", 1200, 4000, 2000)

# Recalcular proyección
deficit = tdee - calorias_slider
peso_array = peso_actual + (deficit * np.arange(91) / 3500)

# Graficar y guardar
fig, ax = plt.subplots()
ax.plot(peso_array, label="Proyección de peso (lbs)", color="blue")
ax.set_xlabel("Días")
ax.set_ylabel("Peso (lbs)")
ax.set_title("Proyección de peso en 3 meses")
ax.grid(True)
plt.tight_layout()
plt.savefig("proyeccion.png")

# Mostrar en Streamlit
st.image("proyeccion.png", caption="Proyección de peso en 90 días")
