## 📐 Descripción Analítica y Técnica

### 📑 1. Arquitectura de Datos y Flujo de Procesamiento
La aplicación opera bajo un flujo reactivo optimizado en **Streamlit**, procesando variables antropométricas y metabólicas de entrada en tiempo real sin requerir almacenamiento persistente de datos del paciente (estatales/en memoria).


Aquí tienes una propuesta para la sección de **Descripción Analítica y Técnica** de tu `README.md`.

Esta estructura está redactada con rigor técnico y enfoque metodológico, ideal para destacar en GitHub o en un portafolio profesional de ciencia de datos y desarrollo analítico.

---

### 📝 Bloque para copiar en tu `README.md`

```markdown
## 📐 Descripción Analítica y Técnica

### 📑 1. Arquitectura de Datos y Flujo de Procesamiento
La aplicación opera bajo un flujo reactivo optimizado en **Streamlit**, procesando variables antropométricas y metabólicas de entrada en tiempo real sin requerir almacenamiento persistente de datos del paciente (estatales/en memoria).


```

[ Inputs del Usuario ] ➔ [ Normalización de Variables ] ➔ [ Motor Algorítmico / Reglas ] ➔ [ Renderizado Plotly & CSS ]

```

1. **Ingesta de Datos:** Captura interactiva de variables cuantitativas (edad, peso en kg, talla en cm) y cualitativas (género, nivel de actividad física, objetivo biológico).
2. **Normalización y Conversión:** Transformación de la altura a metros para evitar sesgos de escala en el cálculo exponencial.
3. **Procesamiento Algorítmico:** Evaluación simultánea de métricas de composición corporal y gasto energético total (GET).
4. **Visualización Reactiva:** Generación dinámica de gráficos vectoriales interactivos con **Plotly Engine** y tarjetas de métricas personalizadas mediante inyección de CSS.

---

### 🧮 2. Metodología y Fundamento Matemático

#### A. Índice de Masa Corporal (IMC) y Rango de Peso
El cálculo del IMC se basa en el estándar antropométrico internacional:

$$\text{IMC} = \frac{\text{Peso (kg)}}{\text{Estatura (m)}^2}$$

* **Estratificación OMS:** Clasificación ordinal en 6 tramos (*Bajo Peso, Normal, Sobrepeso, Obesidad I, II y III*) vinculada dinámicamente a una paleta de colores cromática de alerta visual (`#29b6f6` a `#b71c1c`).
* **Límites de Peso Saludable:** Determinación de las fronteras inferior y superior tomando como referencia la franja eufórica de la OMS ($18.5 \le \text{IMC} \le 24.9$):
  $$\text{Peso}_{\text{min}} = 18.5 \times \text{Estatura}^2 \quad | \quad \text{Peso}_{\text{max}} = 24.9 \times \text{Estatura}^2$$

#### B. Tasa Metabólica Basal (TMB) y Gasto Energético Total (GET)
Se implementa la **Ecuación de Mifflin-St Jeor**, reconocida por su alta precisión en poblaciones adultas contemporáneas:

* **Varones:** 
  $$\text{TMB} = (10 \times \text{Peso}) + (6.25 \times \text{Estatura}_{\text{cm}}) - (5 \times \text{Edad}) + 5$$
* **Mujeres:** 
  $$\text{TMB} = (10 \times \text{Peso}) + (6.25 \times \text{Estatura}_{\text{cm}}) - (5 \times \text{Edad}) - 161$$

El **Gasto Energético Total (GET)** o calorías de mantenimiento se obtiene aplicando el factor de actividad física $FA \in [1.2, 1.9]$:

$$\text{GET} = \text{TMB} \times FA$$

#### C. Prescripción Calórica por Objetivo
Aplicación de un algoritmo de ajuste calórico basado en el balance energético:
* **Déficit Calórico (Pérdida de Grasa):** $\text{GET} - 500 \text{ kcal/día}$
* **Superávit Calórico (Masa Muscular):** $\text{GET} + 300 \text{ kcal/día}$
* **Mantenimiento:** $\text{GET}$

---

### 🎨 3. Componentes Visuales e Interacción User Interface (UI)

* **Plotly Gauge Chart (Velocímetro):** Implementación de un gráfico indicador ordinal tipo velocímetro (`go.Indicator`) con zonas de peligro codificadas por colores, aguja marcadora exacta y límite de umbral para diagnóstico visual inmediato.
* **Plotly Bar Chart Horizontal:** Representación gráfica comparativa de la posición actual del paciente frente a los límites mínimos y máximos saludables de peso corporal.
* **Módulos Card CSS Personalizados:** Inyección de estilos HTML/CSS mediante `st.markdown(unsafe_allow_html=True)` para presentar KPIs destacados con bordes dinámicos condicionales según el estado de salud.
* **Motor Inferencial de Recomendaciones:** Sistema de reglas condicionales (`if-else logic`) para prescribir pautas nutricionales y de ejercicio según la categoría del IMC y el nivel de sedentarismo.

```
