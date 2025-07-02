st.set_page_config(page_title="Calculadora de Calorías y TDEE", layout="centered")

st.title("🔥 Calculadora de Calorías, TDEE y Proyección de Peso")

# Datos personales
nombre = st.text_input("Nombre:")
edad = st.number_input("Edad", min_value=10, max_value=100, step=1)
genero = st.selectbox("Género", ["Masculino", "Femenino"])
peso_lbs = st.number_input("Peso (libras)", min_value=50.0, max_value=500.0, step=0.5)
altura_pulg = st.number_input("Altura (pulgadas)", min_value=50.0, max_value=100.0, step=0.5)
actividad = st.selectbox("Nivel de actividad física", [
    "Sedentario (poco o nada de ejercicio)",
    "Ligero (ejercicio ligero 1-3 días/semana)",
    "Moderado (ejercicio moderado 3-5 días/semana)",
    "Activo (ejercicio fuerte 6-7 días/semana)",
    "Muy activo (ejercicio intenso diario + trabajo físico)"
])

objetivo = st.selectbox("Objetivo", [
    "Perder peso",
    "Mantener peso",
    "Ganar músculo"
])

# Convertir unidades
peso_kg = peso_lbs * 0.453592
altura_cm = altura_pulg * 2.54

# Calcular TMB
if genero == "Masculino":
    tmb = 10 * peso_kg + 6.25 * altura_cm - 5 * edad + 5
else:
    tmb = 10 * peso_kg + 6.25 * altura_cm - 5 * edad - 161

# Multiplicador de actividad
niveles = {
    "Sedentario (poco o nada de ejercicio)": 1.2,
    "Ligero (ejercicio ligero 1-3 días/semana)": 1.375,
    "Moderado (ejercicio moderado 3-5 días/semana)": 1.55,
    "Activo (ejercicio fuerte 6-7 días/semana)": 1.725,
    "Muy activo (ejercicio intenso diario + trabajo físico)": 1.9
}
tdee = tmb * niveles[actividad]

# Calorías según objetivo
mantener = round(tdee)
perder = round(tdee - 500)
ganar = round(tdee + 500)

# Mostrar resultados
if st.button("Calcular TDEE y Calorías"):
    st.subheader(f"Resultados para {nombre}")
    st.write(f"Tu TMB (Tasa Metabólica Basal): **{round(tmb)} kcal/día**")
    st.write(f"Tu TDEE (Calorías para mantener tu peso): **{mantener} kcal/día**")

    st.markdown("### Calorías diarias según tu objetivo:")
    st.info(f"🔵 Mantener peso: **{mantener} kcal**")
    st.success(f"🟢 Perder peso: **{perder} kcal**")
    st.warning(f"🟠 Ganar músculo: **{ganar} kcal**")

    # Proyección de peso
    semanas = list(range(0, 13))
    peso_actual = peso_lbs
    proyeccion = []

    for semana in semanas:
        if objetivo == "Perder peso":
            peso = peso_actual - (semana * 1)  # 1 lb por semana
        elif objetivo == "Ganar músculo":
            peso = peso_actual + (semana * 0.5)  # 0.5 lb por semana
        else:
            peso = peso_actual  # mantener
        proyeccion.append(max(peso, 0))

    df = pd.DataFrame({"Semana": semanas, "Peso estimado (lbs)": proyeccion})

    # Gráfica
    st.markdown("### 📈 Proyección de peso (12 semanas)")
    fig, ax = plt.subplots()
    ax.plot(df["Semana"], df["Peso estimado (lbs)"], marker="o")
    ax.set_xlabel("Semana")
    ax.set_ylabel("Peso estimado (lbs)")
    ax.set_title(f"Proyección de peso para {objetivo}")
    st.pyplot(fig)
