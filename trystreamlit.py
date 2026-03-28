import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def cargar_datos():
    return pd.read_csv("datos_limpios.csv")

df = cargar_datos()

st.set_page_config(page_title="Banking Risk Simulator", layout="wide")
st.title("Simulador de Riesgo Crediticio Bancario")

with st.sidebar:
    st.header("Configuración del Crédito")
    monto = st.number_input("Monto del Préstamo ($)", min_value=1000, value=30000, step=1000, max_value=1000000)
    tasa_anual = st.slider("Tasa Anual (%)", 1.0, 50.0, 12.0)
    plazo = st.selectbox("Plazo (Meses)", [12, 24, 36, 48, 60])
    metodo = st.radio("Sistema de Amortización", ["Alemán", "Francés", "Americano"])

tasa_mensual = (tasa_anual / 100) / 12

if metodo == "Alemán":
    cuota = (monto / plazo) + (monto * tasa_mensual)
elif metodo == "Francés":
    cuota = monto * (tasa_mensual * (1 + tasa_mensual)**plazo) / ((1 + tasa_mensual)**plazo - 1)
else:
    cuota = monto * tasa_mensual

df['nueva_cuota'] = cuota
df['nuevo_dti'] = ((df['debt_ratio'] * df['monthly_income']) + cuota) / df['monthly_income']
df['decision'] = np.where((df['nuevo_dti'] > 0.45) | (df['late_90'] > 0), "RECHAZADO", "APROBADO")

col1, col2= st.columns(2)
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)
col7, col8 = st.columns(2)

with col1:
    aprobados = len(df[df['decision'] == 'APROBADO'])
    st.metric("Total Aprobados", f"{aprobados:,}", border=True)
with col2:
    tasa_aprob = (aprobados / len(df)) * 100
    st.metric("Tasa de Aprobación", f"{tasa_aprob:.2f}%", border=True)
with col3:
    avg_monthly_income = df[df['decision'] == 'APROBADO']['monthly_income'].mean()
    st.metric("Ingreso Mensual Promedio (Aprobados)", f"${avg_monthly_income:,.2f}", border=True)
with col4:
    avg_age = df[df['decision'] == 'APROBADO']['age'].mean()
    st.metric("Edad Promedio (Aprobados)", f"{avg_age:.1f} años", border=True)
with col5:
    capital_riesgo = df[df['decision'] == 'APROBADO']['monthly_income'].sum()
    st.metric("Capital en Riesgo", f"${capital_riesgo:,.2f}", border=True)
with col6:
    ratio_morosidad_aprobados = (df[df['decision'] == 'APROBADO']['late_90'].count() / len(df)) * 100
    st.metric("Ratio Morosidad Histórica (Aprobados)", f"{ratio_morosidad_aprobados:.2f}%", border=True)
with col7:
    margen_interes_proyectado = monto * tasa_mensual * df[df['decision'] == 'APROBADO']['late_90'].count()
    st.metric("Margen de Interés Proyectado (Primer Mes)", f"${margen_interes_proyectado:,.2f}", border=True)

#Gráfico 1
st.subheader("Distribución de Decisiones")
st.bar_chart(df['decision'].value_counts())

#Gráfico 2
fig, ax = plt.subplots()
ax.hist(df[df['decision'] == 'APROBADO']['nuevo_dti'], bins=20, alpha=0.7, label='Aprobados')
ax.set_title("Histograma de Distribución del Nuevo DTI (Debt-to-Income)")
ax.set_xlabel("Riesgo")
ax.set_ylabel("Numero Aprobados")
ax.set_xlim(0, 0.45)

st.pyplot(fig)

#Gráfico 3
with st.expander("Ver Mapa de Riesgo (Plotly)"):
    df_sample = df.sample(n=min(3000, len(df)))
    
    fig = px.scatter(
        df_sample, 
        x='monthly_income', 
        y='nuevo_dti', 
        color='decision',
        labels={'decision': 'Decisión', 'monthly_income': 'Ingreso Mensual', 'nuevo_dti': 'Nuevo DTI'},
        title="Mapa de Riesgo: Ingreso vs Endeudamiento"
    )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5,
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

#Gráfico 4
st.subheader("Análisis de Rechazos")
df_rechazados = df[df['decision'] == 'RECHAZADO']

causas = {
    "Exceso de DTI (>0.45)": (df_rechazados['nuevo_dti'] > 0.45).sum(),
    "Historial de Mora (90+ días)": (df_rechazados['late_90'] > 0).sum(),
    "Sin Ingresos Registrados": (df_rechazados['monthly_income'] == 0).sum()
}
df_causas = pd.DataFrame(causas.items(), columns=['Razón', 'Cantidad'])
st.bar_chart(df_causas, x='Razón', y='Cantidad', horizontal=True)

#Grafico 5
st.subheader("Evolución de la Cuota (Simulación de un cliente)")
meses_lista = list(range(1, plazo+1))
cuotas_simuladas = []

for m in meses_lista:
    if metodo == "Alemán":
        amort_cte = monto / plazo
        interes_mes = (monto - (amort_cte * (m-1))) * tasa_mensual
        cuotas_simuladas.append(amort_cte + interes_mes)
    elif metodo == "Francés":
        cuotas_simuladas.append(cuota)
    else:
        cuotas_simuladas.append(monto * tasa_mensual if m < plazo else monto + (monto * tasa_mensual))

df_curva = pd.DataFrame({'Mes': meses_lista, 'Cuota': cuotas_simuladas})
st.line_chart(df_curva, x='Mes', y='Cuota')