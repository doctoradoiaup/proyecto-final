# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 10:27:49 2024

@author: jperezr
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import MultiComparison

# Título de la aplicación
#st.title("ANOVA y LSD para prueba de hipótesis de un factor con más de 2 grupos")


st.title("Estadística para la investigación")
st.subheader("Proyecto final: Análisis de Precios de Acciones de AAPL")
st.write("Nombre: Javier Horacio Pérez Ricárdez")

st.subheader("Sección VI.- Análisis de Precios de Acciones de AAPL usando ANOVA y LSD")

st.write("""
    Esta aplicación permite seleccionar muestras de precios de acciones de AAPL en diferentes rangos de fechas,
    con el fin de realizar un análisis de varianza (ANOVA) y pruebas LSD para comparar si existen diferencias significativas
    entre los precios seleccionados en diferentes periodos.
""")

# Descargar los datos de AAPL desde Yahoo Finance
data = yf.download("AAPL", start="2020-01-01", end="2024-01-01")
data.reset_index(inplace=True)

# Convertir la columna de fechas a formato datetime
data['Date'] = pd.to_datetime(data['Date'])

# Muestras para el Grupo A
st.header("Seleccionar Fechas para Grupo A")
sample_date_a_start = st.date_input("Fecha de inicio para Grupo A", value=pd.to_datetime("2020-02-01").date())
sample_date_a_end = st.date_input("Fecha de fin para Grupo A", value=pd.to_datetime("2020-04-01").date())

# Filtrar los datos de AAPL para Grupo A
group_a = data[(data['Date'] >= pd.to_datetime(sample_date_a_start)) & (data['Date'] <= pd.to_datetime(sample_date_a_end))][['Date', 'Close']].reset_index(drop=True)

# Mostrar DataFrame para Grupo A
st.subheader("Muestra del Grupo A (Precios de AAPL entre las fechas seleccionadas)")
if not group_a.empty:
    st.dataframe(group_a)
else:
    st.write("No hay datos para Grupo A en el rango seleccionado.")

# Muestras para el Grupo B
st.header("Seleccionar Fechas para Grupo B")
sample_date_b_start = st.date_input("Fecha de inicio para Grupo B", value=pd.to_datetime("2021-01-01").date())
sample_date_b_end = st.date_input("Fecha de fin para Grupo B", value=pd.to_datetime("2021-03-01").date())

# Filtrar los datos de AAPL para Grupo B
group_b = data[(data['Date'] >= pd.to_datetime(sample_date_b_start)) & (data['Date'] <= pd.to_datetime(sample_date_b_end))][['Date', 'Close']].reset_index(drop=True)

# Mostrar DataFrame para Grupo B
st.subheader("Muestra del Grupo B (Precios de AAPL entre las fechas seleccionadas)")
if not group_b.empty:
    st.dataframe(group_b)
else:
    st.write("No hay datos para Grupo B en el rango seleccionado.")

# Muestras para el Grupo C
st.header("Seleccionar Fechas para Grupo C")
sample_date_c_start = st.date_input("Fecha de inicio para Grupo C", value=pd.to_datetime("2022-05-01").date())
sample_date_c_end = st.date_input("Fecha de fin para Grupo C", value=pd.to_datetime("2022-07-01").date())

# Filtrar los datos de AAPL para Grupo C
group_c = data[(data['Date'] >= pd.to_datetime(sample_date_c_start)) & (data['Date'] <= pd.to_datetime(sample_date_c_end))][['Date', 'Close']].reset_index(drop=True)

# Mostrar DataFrame para Grupo C
st.subheader("Muestra del Grupo C (Precios de AAPL entre las fechas seleccionadas)")
if not group_c.empty:
    st.dataframe(group_c)
else:
    st.write("No hay datos para Grupo C en el rango seleccionado.")

# Realizar el análisis solo si los tres grupos tienen datos
if not group_a.empty and not group_b.empty and not group_c.empty:
    # Preparar los datos para ANOVA
    anova_data = pd.DataFrame({
        'Grupo': ['A'] * len(group_a) + ['B'] * len(group_b) + ['C'] * len(group_c),
        'Valores': np.concatenate([group_a['Close'], group_b['Close'], group_c['Close']])
    })

    # Realizar ANOVA
    anova_model = ols('Valores ~ Grupo', data=anova_data).fit()
    anova_table = sm.stats.anova_lm(anova_model, typ=2)

    # Mostrar resultados del ANOVA
    st.subheader("Resultados del ANOVA")
    st.write(anova_table)

    # Grados de libertad y cálculo del LSD
    df_within = anova_table["df"].sum() - anova_table["df"].max()  # Grados de libertad dentro
    ms_within = anova_table["sum_sq"].sum() / df_within  # Media de cuadrados dentro

    # Obtener el valor crítico t
    t_crit = stats.t.ppf(1 - 0.025, df_within)  # Valor crítico t con un nivel de significancia de 0.05

    # Calcular el valor de LSD
    n_a, n_b, n_c = len(group_a), len(group_b), len(group_c)
    lsd_value = t_crit * np.sqrt(ms_within * (1/n_a + 1/n_b + 1/n_c))

    # Mostrar valor de LSD
    st.subheader(f"Valor de LSD: {lsd_value:.4f}")

    # Cálculos de diferencia entre medias
    mean_diff_ab = np.abs(group_a['Close'].mean() - group_b['Close'].mean())
    mean_diff_ac = np.abs(group_a['Close'].mean() - group_c['Close'].mean())
    mean_diff_bc = np.abs(group_b['Close'].mean() - group_c['Close'].mean())

    # Mostrar diferencias entre medias y si son significativas
    st.subheader("Diferencias entre Medias")
    st.write(f"Diferencia entre A y B: {mean_diff_ab:.4f} (Estadístico Crítico: {lsd_value:.4f}) {'(Significativa)' if mean_diff_ab > lsd_value else '(No significativa)'}")
    st.write(f"Diferencia entre A y C: {mean_diff_ac:.4f} (Estadístico Crítico: {lsd_value:.4f}) {'(Significativa)' if mean_diff_ac > lsd_value else '(No significativa)'}")
    st.write(f"Diferencia entre B y C: {mean_diff_bc:.4f} (Estadístico Crítico: {lsd_value:.4f}) {'(Significativa)' if mean_diff_bc > lsd_value else '(No significativa)'}")

    # Gráfico de barras para las diferencias entre medias
    st.subheader("Gráfico de Diferencias entre Medias")
    fig, ax = plt.subplots()

    # Crear el gráfico de barras
    diferencias = [mean_diff_ab, mean_diff_ac, mean_diff_bc]
    grupos = ['A vs B', 'A vs C', 'B vs C']
    colores = ['green' if diff > lsd_value else 'red' for diff in diferencias]

    ax.bar(grupos, diferencias, color=colores)
    ax.axhline(lsd_value, color='blue', linestyle='--', label=f'Valor Crítico LSD: {lsd_value:.4f}')

    ax.set_ylabel('Diferencia de Medias')
    ax.set_title('Comparación de Diferencias entre Medias y Valor Crítico LSD')
    ax.legend()

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

    # Mostrar conclusión sobre las hipótesis
    st.subheader("Conclusión de la Prueba")
    st.write("Si la diferencia es mayor que el estadístico crítico, se rechaza la hipótesis nula, indicando que hay una diferencia significativa entre las medias.")
    st.write("De lo contrario, se acepta la hipótesis nula, indicando que no hay diferencia significativa.")

else:
    st.write("Por favor, selecciona fechas válidas para todos los grupos para realizar el análisis ANOVA.")
