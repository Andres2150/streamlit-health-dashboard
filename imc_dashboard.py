import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# CONFIGURACIÓN DE PÁGINA (Única y al inicio)
# ==========================================
st.set_page_config(
    page_title="Dashboard Integral de Salud & IMC",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# ESTILOS CSS PARA OPTIMIZACIÓN VISUAL
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
    .metric-subtext {
        font-size: 0.8rem;
        color: #495057;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# ENCABEZADO PRINCIPAL
# ---------------------------------------------------------
st.title("🩺 Dashboard de Salud y Evaluación Antropométrica")
st.caption(
    "Herramienta independiente para evaluación metabólica, control de peso e IMC."
)
st.markdown("---")

# ---------------------------------------------------------
# SIDEBAR - INGRESO DE DATOS DEL PACIENTE
# ---------------------------------------------------------
st.sidebar.header("👤 Datos del Paciente")

genero = st.sidebar.selectbox("Género", ["Masculino", "Femenino"])
edad = st.sidebar.number_input("Edad (años)", min_value=10, max_value=120, value=30, step=1)
estatura_cm = st.sidebar.number_input("Estatura (cm)", min_value=100.0, max_value=250.0, value=175.0, step=0.5)
peso_kg = st.sidebar.number_input("Peso Actual (kg)", min_value=30.0, max_value=250.0, value=82.0, step=0.5)

actividad = st.sidebar.selectbox(
    "Nivel de Actividad Física",
    [
        "Sedentario (poco o ningún ejercicio)",
        "Lígero (ejercicio 1-3 días/semana)",
        "Moderado (ejercicio 3-5 días/semana)",
        "Intenso (ejercicio 6-7 días/semana)",
        "Muy Intenso (ejercicio atleta / trabajo físico)"
    ]
)

objetivo = st.sidebar.selectbox(
    "Objetivo Nutricional",
    ["Mantenimiento de Peso", "Pérdida de Peso (Déficit)", "Ganancia Muscular (Superávit)"]
)

# ---------------------------------------------------------
# CÁLCULOS METABÓLICOS Y ANTROPOMÉTRICOS
# ---------------------------------------------------------
estatura_m = estatura_cm / 100.0
imc = peso_kg / (estatura_m ** 2)

# Clasificación según la Organización Mundial de la Salud (OMS)
if imc < 18.5:
    clasificacion_oms = "Bajo Peso"
    color_oms = "#29b6f6"  # Azul
elif 18.5 <= imc < 25.0:
    clasificacion_oms = "Peso Normal (Saludable)"
    color_oms = "#66bb6a"  # Verde
elif 25.0 <= imc < 30.0:
    clasificacion_oms = "Sobrepeso"
    color_oms = "#ffa726"  # Naranja
elif 30.0 <= imc < 35.0:
    clasificacion_oms = "Obesidad Grado I"
    color_oms = "#ef5350"  # Rojo claro
elif 35.0 <= imc < 40.0:
    clasificacion_oms = "Obesidad Grado II"
    color_oms = "#e53935"  # Rojo
else:
    clasificacion_oms = "Obesidad Grado III (Mórbida)"
    color_oms = "#b71c1c"  # Rojo oscuro

# Rangos de Peso Ideal OMS (18.5 a 24.9 kg/m²)
peso_ideal_min = round(18.5 * (estatura_m ** 2), 1)
peso_ideal_max = round(24.9 * (estatura_m ** 2), 1)

kilos_por_perder = max(0.0, peso_kg - peso_ideal_max)
kilos_por_ganar = max(0.0, peso_ideal_min - peso_kg)

# Tasa Metabólica Basal (Fórmula de Mifflin-St Jeor)
if genero == "Masculino":
    tmb = (10 * peso_kg) + (6.25 * estatura_cm) - (5 * edad) + 5
else:
    tmb = (10 * peso_kg) + (6.25 * estatura_cm) - (5 * edad) - 161

# Gasto Energético Total (GET)
factores_actividad = {
    "Sedentario (poco o ningún ejercicio)": 1.2,
    "Lígero (ejercicio 1-3 días/semana)": 1.375,
    "Moderado (ejercicio 3-5 días/semana)": 1.55,
    "Intenso (ejercicio 6-7 días/semana)": 1.725,
    "Muy Intenso (ejercicio atleta / trabajo físico)": 1.9
}
factor = factores_actividad[actividad]
calorias_mantenimiento = tmb * factor

# Calorías recomendadas según objetivo
if objetivo == "Pérdida de Peso (Déficit)":
    calorias_recomendadas = calorias_mantenimiento - 500
elif objetivo == "Ganancia Muscular (Superávit)":
    calorias_recomendadas = calorias_mantenimiento + 300
else:
    calorias_recomendadas = calorias_mantenimiento

# ---------------------------------------------------------
# BLOQUE 1: VELOCÍMETRO DE IMC & EVALUACIÓN DE PESO
# ---------------------------------------------------------
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📊 Velocímetro IMC (Plotly Gauge)")
    
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=imc,
        number={'suffix': " kg/m²", 'font': {'size': 26}},
        title={'text': f"Clasificación OMS: <b>{clasificacion_oms}</b>", 'font': {'size': 16, 'color': color_oms}},
        gauge={
            'axis': {'range': [10, 45], 'tickwidth': 1, 'tickcolor': "#333333"},
            'bar': {'color': "#111111", 'width': 3},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#cccccc",
            'steps': [
                {'range': [10, 18.5], 'color': '#29b6f6'},
                {'range': [18.5, 25], 'color': '#66bb6a'},
                {'range': [25, 30], 'color': '#ffa726'},
                {'range': [30, 35], 'color': '#ef5350'},
                {'range': [35, 45], 'color': '#b71c1c'}
            ],
            'threshold': {
                'line': {'color': "#000000", 'width': 4},
                'thickness': 0.75,
                'value': imc
            }
        }
    ))
    fig_gauge.update_layout(
        height=290,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

with col2:
    st.subheader("⚖️ Evaluación de Peso Ideal")
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Rango de Peso Saludable (OMS)</div>
        <div class="metric-value">{peso_ideal_min} kg – {peso_ideal_max} kg</div>
        <div class="metric-subtext">Basado en un IMC de 18.5 a 24.9 kg/m²</div>
    </div>
    """, unsafe_allow_html=True)

    if kilos_por_perder > 0:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #ef5350;">
            <div class="metric-title">Exceso de Peso Estimado</div>
            <div class="metric-value" style="color: #c62828;">-{kilos_por_perder:.1f} kg</div>
            <div class="metric-subtext">Kilos por encima del límite superior saludable</div>
        </div>
        """, unsafe_allow_html=True)
    elif kilos_por_ganar > 0:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #0288d1;">
            <div class="metric-title">Déficit de Peso Estimado</div>
            <div class="metric-value" style="color: #0277bd;">+{kilos_por_ganar:.1f} kg</div>
            <div class="metric-subtext">Kilos necesarios para ingresar al rango normal</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="metric-card" style="border-left-color: #43a047;">
            <div class="metric-title">Estado del Peso</div>
            <div class="metric-value" style="color: #2e7d32;">¡En Rango Óptimo!</div>
            <div class="metric-subtext">Su peso está perfectamente dentro del rango saludable.</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------------
# BLOQUE 2: METABOLISMO, CALORÍAS Y RANGO SALUDABLE
# ---------------------------------------------------------
col3, col4 = st.columns([1, 1])

with col3:
    st.subheader("🔥 Metabolismo y Calorías Diarias")
    
    m1, m2 = st.columns(2)
    with m1:
        st.metric(
            label="Metabolismo Basal (TMB)",
            value=f"{int(tmb)} kcal/día",
            help="Gasto calórico del organismo en reposo absoluto."
        )
    with m2:
        st.metric(
            label="Gasto Diario Total (GET)",
            value=f"{int(calorias_mantenimiento)} kcal/día",
            help="Gasto calórico total según su nivel de actividad."
        )

    st.markdown(f"""
    <div style="background-color: #e3f2fd; padding: 15px; border-radius: 8px; border-left: 5px solid #1e88e5;">
        <h4 style="margin:0; color:#1565c0;">🍽️ Calorías Diarias Recomendadas</h4>
        <p style="font-size: 1.8rem; font-weight: bold; margin: 5px 0; color: #0d47a1;">{int(calorias_recomendadas)} kcal/día</p>
        <span style="font-size: 0.85rem; color: #424242;">Objetivo seleccionado: <b>{objetivo}</b></span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.subheader("📉 Gráfico del Rango Saludable")
    
    df_peso = pd.DataFrame({
        'Categoría': ['Límite Inferior Ideal', 'Peso Actual', 'Límite Superior Ideal'],
        'Peso (kg)': [peso_ideal_min, peso_kg, peso_ideal_max],
        'Tipo': ['Rango Saludable', 'Paciente', 'Rango Saludable']
    })

    fig_bar = px.bar(
        df_peso,
        x='Peso (kg)',
        y='Categoría',
        orientation='h',
        text='Peso (kg)',
        color='Tipo',
        color_discrete_map={'Rango Saludable': '#a5d6a7', 'Paciente': color_oms},
        title="Comparativa: Peso Actual vs. Límites Saludables"
    )
    fig_bar.update_traces(texttemplate='%{text:.1f} kg', textposition='outside')
    fig_bar.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False,
        xaxis=dict(range=[0, max(peso_kg, peso_ideal_max) * 1.25])
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------
# BLOQUE 3: RECOMENDACIONES PERSONALIZADAS
# ---------------------------------------------------------
st.subheader("📋 Recomendaciones Personalizadas")

rec_col1, rec_col2 = st.columns(2)

with rec_col1:
    st.markdown("##### 🥗 Estrategia Nutricional")
    if imc >= 25.0:
        st.markdown("""
        * **Déficit Calórico Estructurado:** Planificar una reducción moderada de 300 a 500 kcal respecto al gasto diario total.
        * **Proteína Suficiente:** Garantizar una ingesta proteica (1.6g – 2.0g/kg) para preservar la masa libre de grasa.
        * **Calidad Nutricional:** Aumentar el volumen de verduras, hortalizas, legumbres y carbohidratos de bajo índice glucémico.
        """)
    elif imc < 18.5:
        st.markdown("""
        * **Superávit Calórico Progresivo:** Incrementar la ingesta en 300 a 500 kcal diarias con alimentos densos en nutrientes.
        * **Frecuencia Regular:** Realizar de 4 a 5 comidas diarias incorporando grasas saludables (frutos secos, palta, aceite de oliva).
        """)
    else:
        st.markdown("""
        * **Mantenimiento Energético:** Consolidar el aporte calórico actual equilibrando macronutrientes.
        * **Variedad de Micronutrientes:** Mantener consumo variado de frutas, verduras de estación y fuentes de fibra.
        """)

with rec_col2:
    st.markdown("##### 🏋️ Prescripción de Actividad Física")
    if actividad in ["Sedentario (poco o ningún ejercicio)", "Lígero (ejercicio 1-3 días/semana)"]:
        st.markdown("""
        * **Activación Progresiva:** Acumular mínimo 150 minutos semanales de actividad aeróbica de intensidad moderada.
        * **Entrenamiento de Fuerza:** Iniciar rutinas de fuerza de 2 a 3 días por semana para mejorar la sensibilidad a la insulina.
        """)
    else:
        st.markdown("""
        * **Programa Híbrido:** Combinar trabajo de hipertrofia/fuerza con periodos intermitentes de alta intensidad (HIIT).
        * **Recuperación:** Garantizar un descanso adecuado (7-8 horas de sueño) para optimizar la síntesis proteica.
        """)
