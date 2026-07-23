import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(
    page_title="Evaluación Nutricional & Salud",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# ESTILOS CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #2e7d32;
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #6c757d;
        margin-bottom: 4px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: bold;
        color: #1b5e20;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. MENÚ LATERAL DE NAVEGACIÓN
# ==========================================
st.sidebar.title("📌 Menú lateral")

menu = st.sidebar.radio(
    "Selecciona una sección:",
    [
        "🏠 Inicio",
        "👤 Datos del paciente",
        "📏 Evaluación antropométrica",
        "❤️ Riesgo cardiometabólico",
        "🔥 Gasto energético",
        "🍗 Macronutrientes",
        "💪 Composición corporal",
        "📈 Dashboard",
        "📋 Informe",
    ],
)

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Entrada Rápida / Datos Clave")

# ==========================================
# 3. CAPTURA DE DATOS GLOBAL DEL PACIENTE
# ==========================================
# Guardar en session_state para mantener la reactividad entre menús
if "genero" not in st.session_state:
    st.session_state.genero = "Masculino"
if "edad" not in st.session_state:
    st.session_state.edad = 30
if "estatura_cm" not in st.session_state:
    st.session_state.estatura_cm = 175.0
if "peso_kg" not in st.session_state:
    st.session_state.peso_kg = 82.0

genero = st.sidebar.selectbox(
    "Género",
    ["Masculino", "Femenino"],
    index=0 if st.session_state.genero == "Masculino" else 1,
)
edad = st.sidebar.number_input(
    "Edad (años)", min_value=10, max_value=120, value=st.session_state.edad, step=1
)
estatura_cm = st.sidebar.number_input(
    "Estatura (cm)",
    min_value=100.0,
    max_value=250.0,
    value=st.session_state.estatura_cm,
    step=0.5,
)
peso_kg = st.sidebar.number_input(
    "Peso Actual (kg)",
    min_value=30.0,
    max_value=250.0,
    value=st.session_state.peso_kg,
    step=0.5,
)

# Medidas adicionales para secciones específicas
cintura_cm = st.sidebar.number_input(
    "Circunferencia Cintura (cm)", min_value=40.0, max_value=200.0, value=85.0
)
cadera_cm = st.sidebar.number_input(
    "Circunferencia Cadera (cm)", min_value=40.0, max_value=200.0, value=100.0
)
porcentaje_grasa = st.sidebar.number_input(
    "% Grasa Estimado/DEXA", min_value=3.0, max_value=60.0, value=22.0
)

actividad = st.sidebar.selectbox(
    "Nivel de Actividad Física",
    [
        "Sedentario (poco o ningún ejercicio)",
        "Lígero (ejercicio 1-3 días/semana)",
        "Moderado (ejercicio 3-5 días/semana)",
        "Intenso (ejercicio 6-7 días/semana)",
        "Muy Intenso (ejercicio atleta / trabajo físico)",
    ],
)

objetivo = st.sidebar.selectbox(
    "Objetivo Nutricional",
    [
        "Mantenimiento de Peso",
        "Pérdida de Peso (Déficit)",
        "Ganancia Muscular (Superávit)",
    ],
)

# ==========================================
# 4. MOTOR DE CÁLCULOS CENTRALIZADO
# ==========================================
estatura_m = estatura_cm / 100.0
imc = peso_kg / (estatura_m**2)

# Clasificación OMS
if imc < 18.5:
    clasificacion_oms = "Bajo Peso"
    color_oms = "#29b6f6"
elif 18.5 <= imc < 25.0:
    clasificacion_oms = "Peso Normal (Saludable)"
    color_oms = "#66bb6a"
elif 25.0 <= imc < 30.0:
    clasificacion_oms = "Sobrepeso"
    color_oms = "#ffa726"
elif 30.0 <= imc < 35.0:
    clasificacion_oms = "Obesidad Grado I"
    color_oms = "#ef5350"
elif 35.0 <= imc < 40.0:
    clasificacion_oms = "Obesidad Grado II"
    color_oms = "#e53935"
else:
    clasificacion_oms = "Obesidad Grado III (Mórbida)"
    color_oms = "#b71c1c"

# Pesos Ideales y Ajustados
peso_ideal_min = round(18.5 * (estatura_m**2), 1)
peso_ideal_max = round(24.9 * (estatura_m**2), 1)
peso_ideal_medio = round(21.7 * (estatura_m**2), 1)
peso_ajustado = round(
    peso_ideal_medio + 0.25 * (peso_kg - peso_ideal_medio), 1
)
exceso_peso = max(0.0, peso_kg - peso_ideal_max)

# Superficie Corporal (DuBois)
superficie_corporal = round(
    0.007184 * (estatura_cm**0.725) * (peso_kg**0.425), 2
)

# Gasto Energético (Mifflin-St Jeor)
if genero == "Masculino":
    tmb_mifflin = (10 * peso_kg) + (6.25 * estatura_cm) - (5 * edad) + 5
    tmb_hb = 66.5 + (13.75 * peso_kg) + (5.003 * estatura_cm) - (6.75 * edad)
else:
    tmb_mifflin = (10 * peso_kg) + (6.25 * estatura_cm) - (5 * edad) - 161
    tmb_hb = 655.1 + (9.563 * peso_kg) + (1.850 * estatura_cm) - (4.676 * edad)

tmb_oms = (14.7 * peso_kg) + 496 if genero == "Masculino" else (8.7 * peso_kg) + 829

factores_actividad = {
    "Sedentario (poco o ningún ejercicio)": 1.2,
    "Lígero (ejercicio 1-3 días/semana)": 1.375,
    "Moderado (ejercicio 3-5 días/semana)": 1.55,
    "Intenso (ejercicio 6-7 días/semana)": 1.725,
    "Muy Intenso (ejercicio atleta / trabajo físico)": 1.9,
}
factor = factores_actividad[actividad]
calorias_mantenimiento = tmb_mifflin * factor

# Composición Corporal
masa_grasa_kg = round(peso_kg * (porcentaje_grasa / 100), 1)
masa_magra_kg = round(peso_kg - masa_grasa_kg, 1)

# ==========================================
# 5. RENDERIZADO SEGÚN SECCIÓN SELECCIONADA
# ==========================================

# ---------------------------------------------------------
# 🏠 INICIO
# ---------------------------------------------------------
if menu == "🏠 Inicio":
    st.title("🩺 Sistema Integral de Evaluación Nutricional")
    st.subheader("Bienvenido a la plataforma antropométrica y clínica")
    st.markdown(
        """
    Esta herramienta permite realizar un análisis completo de la composición corporal, metabolismo, 
    riesgo cardiometabólico y requerimientos nutricionales del paciente.
    
    👈 **Navega a través del menú lateral** para acceder a los diferentes módulos de evaluación.
    """
    )

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Estado de Peso", clasificacion_oms)
    col_b.metric("IMC Actual", f"{imc:.1f} kg/m²")
    col_c.metric("GET Estimado", f"{int(calorias_mantenimiento)} kcal/día")

# ---------------------------------------------------------
# 👤 DATOS DEL PACIENTE
# ---------------------------------------------------------
elif menu == "👤 Datos del paciente":
    st.title("👤 Ficha Clínica del Paciente")

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Género:** {genero}")
        st.write(f"**Edad:** {edad} años")
        st.write(f"**Estatura:** {estatura_cm} cm")
        st.write(f"**Peso Actual:** {peso_kg} kg")

    with col2:
        st.write(f"**Nivel de Actividad:** {actividad}")
        st.write(f"**Objetivo Seleccionado:** {objetivo}")
        st.write(f"**Superficie Corporal:** {superficie_corporal} m²")

# ---------------------------------------------------------
# 📏 EVALUACIÓN ANTROPOMÉTRICA
# ---------------------------------------------------------
elif menu == "📏 Evaluación antropométrica":
    st.title("📏 Evaluación Antropométrica")

    col1, col2, col3 = st.columns(3)
    col1.metric("IMC", f"{imc:.1f} kg/m²", delta=clasificacion_oms)
    col2.metric(
        "Peso Ideal (Medio)",
        f"{peso_ideal_medio} kg",
        f"Rango: {peso_ideal_min} - {peso_ideal_max} kg",
    )
    col3.metric("Peso Ajustado", f"{peso_ajustado} kg")

    col4, col5 = st.columns(2)
    col4.metric("Exceso de Peso", f"{exceso_peso:.1f} kg")
    col5.metric("Superficie Corporal (DuBois)", f"{superficie_corporal} m²")

# ---------------------------------------------------------
# ❤️ RIESGO CARDIOMETABÓLICO
# ---------------------------------------------------------
elif menu == "❤️ Riesgo cardiometabólico":
    st.title("❤️ Evaluación de Riesgo Cardiometabólico")

    ica = cintura_cm / estatura_cm
    icc = cintura_cm / cadera_cm

    c1, c2, c3 = st.columns(3)
    c1.metric("Circunferencia Cintura", f"{cintura_cm} cm")
    c2.metric("Índice Cintura/Estatura (ICE)", f"{ica:.2f}")
    c3.metric("Índice Cintura/Cadera (ICC)", f"{icc:.2f}")

    st.subheader("Riesgo Cardiovascular")
    if ica > 0.5:
        st.error(
            "⚠️ **Riesgo Aumentado:** El índice cintura/estatura supera el umbral recomendado (0.50)."
        )
    else:
        st.success("✅ **Riesgo Bajo:** Medidas dentro de los rangos óptimos.")

# ---------------------------------------------------------
# 🔥 GASTO ENERGÉTICO
# ---------------------------------------------------------
elif menu == "🔥 Gasto energético":
    st.title("🔥 Requerimiento y Gasto Energético")

    g1, g2, g3 = st.columns(3)
    g1.metric("Harris-Benedict (TMB)", f"{int(tmb_hb)} kcal")
    g2.metric("Mifflin-St Jeor (TMB)", f"{int(tmb_mifflin)} kcal")
    g3.metric("OMS (TMB)", f"{int(tmb_oms)} kcal")

    st.markdown("---")
    st.subheader("Calorías Según Objetivo")

    col_def, col_man, col_sup = st.columns(3)
    col_def.metric(
        "Déficit Calórico (-500)",
        f"{int(calorias_mantenimiento - 500)} kcal/día",
    )
    col_man.metric(
        "Calorías Mantenimiento", f"{int(calorias_mantenimiento)} kcal/día"
    )
    col_sup.metric(
        "Superávit Calórico (+300)",
        f"{int(calorias_mantenimiento + 300)} kcal/día",
    )

# ---------------------------------------------------------
# 🍗 MACRONUTRIENTES
# ---------------------------------------------------------
elif menu == "🍗 Macronutrientes":
    st.title("🍗 Distribución de Macronutrientes")

    prot_g = round(peso_kg * 2.0, 1)  # 2.0g/kg
    grasas_g = round((calorias_mantenimiento * 0.25) / 9, 1)  # 25% kcal
    carbs_g = round(
        (calorias_mantenimiento - (prot_g * 4 + grasas_g * 9)) / 4, 1
    )
    agua_ml = round(peso_kg * 35, 0)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Proteínas (2g/kg)", f"{prot_g} g/día")
    m2.metric("Grasas (25%)", f"{grasas_g} g/día")
    m3.metric("Carbohidratos", f"{carbs_g} g/día")
    m4.metric("Agua Diaria", f"{agua_ml / 1000:.2f} L/día")

# ---------------------------------------------------------
# 💪 COMPOSICIÓN CORPORAL
# ---------------------------------------------------------
elif menu == "💪 Composición corporal":
    st.title("💪 Análisis de Composición Corporal")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("% Grasa Corporal", f"{porcentaje_grasa}%")
    k2.metric("Masa Grasa", f"{masa_grasa_kg} kg")
    k3.metric("Masa Magra", f"{masa_magra_kg} kg")
    k4.metric("Peso Libre de Grasa", f"{masa_magra_kg} kg")

# ---------------------------------------------------------
# 📈 DASHBOARD
# ---------------------------------------------------------
elif menu == "📈 Dashboard":
    st.title("📈 Dashboard Visores y Gráficos")

    # Gauge Chart
    fig_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=imc,
            title={"text": "Índice de Masa Corporal (IMC)"},
            gauge={
                "axis": {"range": [10, 40]},
                "bar": {"color": "#1f77b4"},
                "steps": [
                    {"range": [10, 18.5], "color": "#29b6f6"},
                    {"range": [18.5, 25.0], "color": "#66bb6a"},
                    {"range": [25.0, 30.0], "color": "#ffa726"},
                    {"range": [30.0, 35.0], "color": "#ef5350"},
                    {"range": [35.0, 40.0], "color": "#b71c1c"},
                ],
            },
        )
    )
    fig_gauge.update_layout(height=300)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_g2:
        df_peso = pd.DataFrame(
            {
                "Categoría": [
                    "Límite Inferior",
                    "Peso Actual",
                    "Límite Superior",
                ],
                "Peso (kg)": [peso_ideal_min, peso_kg, peso_ideal_max],
                "Tipo": ["Saludable", "Paciente", "Saludable"],
            }
        )
        fig_bar = px.bar(
            df_peso,
            x="Peso (kg)",
            y="Categoría",
            orientation="h",
            color="Tipo",
            title="Comparativa de Peso",
        )
        fig_bar.update_layout(height=300)
        st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------------------------------------
# 📋 INFORME
# ---------------------------------------------------------
elif menu == "📋 Informe":
    st.title("📋 Informe Clínico y Recomendaciones")

    st.subheader("Diagnóstico Antropométrico")
    st.write(
        f"El paciente de **{edad} años** presenta un **IMC de {imc:.1f} kg/m²**, clasificando en la categoría de **{clasificacion_oms}**."
    )

    st.subheader("Recomendaciones")
    st.markdown(
        """
    * **Plan Nutricional:** Ajustar la ingesta según el objetivo seleccionado.
    * **Actividad Física:** Combinar ejercicio aeróbico con entrenamiento de fuerza.
    """
    )

    st.button("📄 Descargar PDF (Simulación)")
