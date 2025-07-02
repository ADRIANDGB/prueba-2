import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Calculadora de Calorías y TDEE", layout="centered")

st.title("🔥 Calculadora de TDEE y Proyección de Peso")

# Entradas del usuario
nombre = st.text_input("¿Cuál es tu nombre?")
edad = st.number_input("Edad", min_value=10, max_value=100, value=25)
sexo = st.radio("Sexo", ["Masculino", "Femenino"])
altura = st.number_input("Altura en pulgadas", min_value=48.0, max_value=90.0, value=70.0)
peso_actual = st.number_input("Peso actual en libras", min_value=80.0, max_value=600.0, value=180.0)
nivel_actividad = st.selectbox("Nivel de actividad física", [
    "Sedentario", 
    "Ligera actividad", 
    "Moderadamente activo", 
    "Muy activo", 
    "Extremadamente activo"
])
goal = st.selectbox("Objetivo", ["Perder peso", "Mantener peso", "Ganar músculo"])

# Calcular TDEE
if st.button("Calcular"):

    # Calcular BMR con fórmula Mifflin-St Jeor
    if sexo == "Masculino":
        bmr = 66 + (6.23 * peso_actual) + (12.7 * altura) - (6.8 * edad)
    else:
        bmr = 655 + (4.35 * peso_actual) + (4.7 * altura) - (4.7 * edad)

    # Factor de actividad
    factores = {
        "Sedentario": 1.2,
        "Ligera actividad": 1.375,
        "Moderadamente activo": 1.55,
        "Muy activo": 1.725,
        "Extremadamente activo": 1.9
    }

    tdee = bmr * factores[nivel_actividad]

    # Calorías sugeridas según objetivo
    mantener = round(tdee)
    perder_peso = round(tdee - 500)
    ganar_musculo = round(tdee + 300)

    st.markdown(f"### 🔍 Resultados para {nombre}")
    st.write(f"**Tu TDEE estimado es:** {tdee:.0f} kcal/día")
    
    if goal == "Perder peso":
        st.info(f"Para perder peso: **{perder_peso} kcal/día** (déficit de 500)")
    elif goal == "Ganar músculo":
        st.info(f"Para ganar músculo: **{ganar_musculo} kcal/día** (superávit de 300)")
    else:
        st.info(f"Para mantener peso: **{mantener} kcal/día**")

    # Slider para ajustar ingesta calórica
    calorias_slider = st.slider("¿Cuántas calorías planeas consumir por día?", 1200, 4000, mantener)

    # Cálculo del déficit o superávit
    diferencia = calorias_slider - mantener
    dias = np.arange(0, 91)
    calorias_por_libra = 3500  # 1 libra = 3500 kcal aprox
    cambio_peso = diferencia * dias / calorias_por_libra
    peso_proyectado = peso_actual + cambio_peso

    # Mostrar estimación
    if diferencia < 0:
        st.warning(f"Déficit de {abs(diferencia)} kcal/día. Posible pérdida de peso.")
    elif diferencia > 0:
        st.success(f"Superávit de {diferencia} kcal/día. Posible ganancia muscular.")
    else:
        st.info("Estás en equilibrio calórico. Mantendrás tu peso.")

    # Crear la gráfica
    fig, ax = plt.subplots()
    ax.plot(dias, peso_proyectado, color='blue', linewidth=2)
    ax.set_title("📊 Proyección de peso en 3 meses")
    ax.set_xlabel("Días")
    ax.set_ylabel("Peso (lbs)")
    ax.grid(True)

    # Guardar y mostrar imagen PNG
    plt.tight_layout()
    plt.savefig("proyeccion_peso.png")
    st.image("proyeccion_peso.png", caption="Proyección de peso (estimado)")
