<div align="center">

  # 🩺 Health & BMI Analytics Dashboard

  **Plataforma Interactiva para la Evaluación Antropométrica, Cálculo Metabólico y Optimización Nutricional**

  [![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
  [![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 📌 Visión General

**Health & BMI Analytics Dashboard** es una solución analítica web desarrollada con **Streamlit** y **Plotly** para el cálculo preciso y diagnóstico dinámico de métricas antropométricas y metabólicas clave. 

La herramienta traduce estándares clínicos internacionales (OMS) en una interfaz intuitiva y reactiva que proporciona alertas visuales, rangos de peso objetivo y recomendaciones calóricas personalizadas en tiempo real.

---

## ✨ Características Principales

- 📊 **Gauge de IMC Interactivo:** Velocímetro visual que categoriza dinámicamente el estado nutricional según la escala OMS.
- ⚖️ **Análisis de Peso Saludable:** Cálculo automático de límites de peso (mínimo, ideal y máximo) junto con el delta de kilos a ganar o perder.
- 🔥 **Gasto Calórico Diario (TMB & GET):** Estimación metabólica mediante el algoritmo de *Mifflin-St Jeor*.
- 🍽️ **Planificación de Objetivos Calóricos:** Ajustes calculados para déficit (pérdida de grasa), mantenimiento o superávit (ganancia muscular).
- 📉 **Gráficos Comparativos Reactivos:** Módulos visuales construidos con Plotly Engine.
- 💡 **Motor Inferencial de Recomendaciones:** Sugerencias automáticas personalizadas según nivel de actividad y perfil antropométrico.

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Descripción / Rol |
| :--- | :--- |
| **Python 3.10+** | Lenguaje principal de procesamiento de datos |
| **Streamlit** | Framework web reactivo para la interfaz de usuario |
| **Plotly** | Renderizado de gráficos interactivos vectoriales |
| **Pandas** | Estructuración y manipulación de datos |

---

## 📐 Descripción Analítica y Técnica

### 📑 1. Arquitectura de Procesamiento

```text
[ Inputs del Usuario ] ➔ [ Normalización ] ➔ [ Motor Algorítmico ] ➔ [ Visualización Plotly & UI ]
