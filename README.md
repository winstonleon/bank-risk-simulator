# 🏦 Banking Risk Simulator & Credit Scoring Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Managed-4169E1?logo=postgresql)

Este proyecto desarrolla un **Pipeline de Ingeniería de Datos** completo para la evaluación de riesgo crediticio, procesando una cartera de **150,000 registros** de clientes reales.

## Funcionalidades Clave
- **Simulador Multimétodo:** Evaluación en tiempo real bajo los sistemas de amortización **Alemán, Francés y Americano**.
- **Cálculo de Stress-Test:** Motor de decisión basado en el ratio **DTI (Debt-to-Income)** con umbral crítico de 0.45.
- **Análisis de Morosidad:** Filtrado automático basado en historial de impagos (90+ días).
- **Visualización Avanzada:** Dashboards interactivos desarrollados con **Plotly** y **Streamlit**.

## Stack Tecnológico
- **Extracción & Limpieza:** Python (Pandas, Numpy) y SQL (PostgreSQL).
- **Backend de Riesgo:** Lógica financiera programada en Python para simulación de cuotas variables.
- **Frontend:** Streamlit para la interfaz de usuario interactiva.
- **Despliegue:** GitHub & Streamlit Cloud.

## Estructura del Proyecto
- `trystreamlit.py`: Aplicación principal y lógica de negocio.
- `datos_limpios.csv`: Dataset procesado tras limpieza ETL en SQL/Python.
- `requirements.txt`: Dependencias del entorno de producción.

---
**Desarrollado por ByJohn** *Estudiante de Ingeniería de Sistemas - UPC*