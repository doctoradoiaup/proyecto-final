# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 16:23:31 2024

@author: jperezr
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Título de la aplicación
st.title("Estadística para la investigación")
st.subheader("Proyecto final: Análisis de Precios de Acciones de AAPL")
st.write("Nombre: Javier Horacio Pérez Ricárdez")

# Mantener el estado de las fechas y el ComboBox
if 'start_date' not in st.session_state:
    st.session_state.start_date = pd.to_datetime("2020-01-01")

if 'end_date' not in st.session_state:
    st.session_state.end_date = pd.to_datetime("2024-01-01")

# Seleccionar fechas
st.session_state.start_date = st.date_input("Selecciona la fecha de inicio", st.session_state.start_date)
st.session_state.end_date = st.date_input("Selecciona la fecha de fin", st.session_state.end_date)

# Descargar datos de Yahoo Finance
ticker = "AAPL"
data = yf.download(ticker, start=st.session_state.start_date, end=st.session_state.end_date)

# Asegurarse de que el índice sea de tipo 'DatetimeIndex'
if not pd.api.types.is_datetime64_any_dtype(data.index):
    data.index = pd.to_datetime(data.index)

# Remover la localización de la zona horaria si existe
data.index = data.index.tz_localize(None)

# Restablecer el índice si necesitas una columna de fecha
data = data.reset_index()  # Esto moverá el índice de fechas a una columna llamada 'Date'

# Mostrar datos descargados
st.subheader("Datos Descargados")
st.write(data)


# Sección II.- Análisis de Distribución
st.subheader("Sección II.- Análisis de Distribución")

# a) Intervalos estadísticos basados en una sola muestra
st.subheader("a) Intervalos Estadísticos Basados en una Sola Muestra")

# Definir la muestra
sample_size = 30  # Tamaño de la muestra
sample_data = data[['Date', 'Close']].sample(n=sample_size, random_state=42)  # Tomar una muestra aleatoria
sample_df = sample_data.reset_index(drop=True)

# Calcular media y desviación estándar
sample_mean = sample_df['Close'].mean()
sample_std = sample_df['Close'].std()

# Calcular el intervalo de confianza del 95%
confidence_level = 0.95
alpha = 1 - confidence_level
critical_value = stats.t.ppf(1 - alpha / 2, df=sample_size - 1)
margin_of_error = critical_value * (sample_std / np.sqrt(sample_size))
confidence_interval = (sample_mean - margin_of_error, sample_mean + margin_of_error)

# Convertir a float antes de mostrar
confidence_interval = (float(confidence_interval[0]), float(confidence_interval[1]))

# Mostrar resultados
st.write("Muestra de datos:")
st.write(sample_df)
st.write(f"Intervalo de confianza del 95% para la media de la muestra: {confidence_interval}")

# Gráfico para visualizar el intervalo de confianza
st.subheader("Gráfico de Intervalo de Confianza para la Media de la Muestra")
plt.figure(figsize=(10, 6))
plt.plot(sample_df['Date'], sample_df['Close'], label="Precio de cierre")
plt.axhline(sample_mean, color='r', linestyle='--', label=f"Media: {sample_mean:.2f}")
plt.fill_between(sample_df['Date'], confidence_interval[0], confidence_interval[1], color='b', alpha=0.2, label=f"Intervalo de Confianza {confidence_level * 100}%")
plt.xlabel("Fecha")
plt.ylabel("Precio de cierre")
plt.legend()
st.pyplot(plt)



# b) Inferencias basadas en dos muestras
st.subheader("b) Inferencias Basadas en Dos Muestras")

# Definir las dos muestras
sample_size_1 = 30
sample_size_2 = 30

# Muestra 1
sample_1 = data[['Date', 'Close']].sample(n=sample_size_1, random_state=42)
sample_1_df = sample_1.reset_index(drop=True)

# Muestra 2
sample_2 = data[['Date', 'Close']].sample(n=sample_size_2, random_state=43)
sample_2_df = sample_2.reset_index(drop=True)

# Mostrar las muestras
st.write("Muestra 1:")
st.write(sample_1_df)
st.write("Muestra 2:")
st.write(sample_2_df)

# Calcular las medias de las muestras
mean_sample_1 = sample_1_df['Close'].mean()
mean_sample_2 = sample_2_df['Close'].mean()

# Mostrar los valores de las medias antes del gráfico
st.subheader("Medias de las dos muestras")
st.write(f"Media de la muestra 1: {mean_sample_1:.2f}")
st.write(f"Media de la muestra 2: {mean_sample_2:.2f}")

# Generar el gráfico de las medias de las dos muestras
fig, ax = plt.subplots()
ax.bar(['Muestra 1', 'Muestra 2'], [mean_sample_1, mean_sample_2], color=['blue', 'green'])
ax.set_ylabel('Precio de Cierre')
ax.set_title('Comparación de Medias entre las Dos Muestras')

# Mostrar el gráfico en Streamlit
st.pyplot(fig)

# Definir hipótesis nula y alternativa
st.write("Hipótesis nula (Ho): Las medias de las dos muestras son iguales.")
st.write("Hipótesis alternativa (Ha): Las medias de las dos muestras son diferentes.")

# Realizar la prueba t para dos muestras
t_stat, p_value = stats.ttest_ind(sample_1['Close'], sample_2['Close'])

# Calcular grados de libertad
df = sample_size_1 + sample_size_2 - 2

# Calcular t crítico
alpha = 0.05
t_crit = stats.t.ppf(1 - alpha / 2, df)

# Mostrar resultados de la prueba
st.write(f"Estadístico t: {t_stat}, p-value: {p_value}")
st.write(f"t crítico (α = {alpha}): {t_crit}")

# Conclusión para el Inciso b)
st.subheader("Conclusión para Inferencias Basadas en Dos Muestras")

if abs(t_stat) > t_crit:
    st.write("Rechazamos la hipótesis nula (Ho).")
    st.write("Esto sugiere que hay una diferencia significativa entre las medias de las dos muestras.")
else:
    st.write("No rechazamos la hipótesis nula (Ho).")
    st.write("Esto sugiere que no hay evidencia suficiente para afirmar que las medias de las dos muestras son diferentes.")
    st.write("Justificación: t < t crítico, lo que indica que la diferencia observada entre las muestras no es suficiente para ser considerada estadísticamente significativa.")



# c) Análisis de varianza (ANOVA)
st.subheader("c) Análisis de Varianza (ANOVA)")

# Crear muestras aleatorias de 'data'
group_a = data[['Date', 'Close']].sample(n=30, random_state=1).reset_index(drop=True)
group_b = data[['Date', 'Close']].sample(n=30, random_state=2).reset_index(drop=True)
group_c = data[['Date', 'Close']].sample(n=30, random_state=3).reset_index(drop=True)

# Mostrar los DataFrames en la aplicación
st.subheader("Muestra del Grupo A")
st.dataframe(group_a)

st.subheader("Muestra del Grupo B")
st.dataframe(group_b)

st.subheader("Muestra del Grupo C")
st.dataframe(group_c)

# Tabular los grupos y sus medias
group_means = pd.DataFrame({
    'Grupo': ['A', 'B', 'C'],
    'Media': [group_a['Close'].mean(), group_b['Close'].mean(), group_c['Close'].mean()]
})
st.subheader("Medias de los Grupos")
st.dataframe(group_means)

# Crear un DataFrame combinado para ANOVA
anova_data = pd.DataFrame({
    'Group': ['A'] * 30 + ['B'] * 30 + ['C'] * 30,
    'Values': np.concatenate([group_a['Close'], group_b['Close'], group_c['Close']])
})

# Realizar el ANOVA
f_statistic, p_value = stats.f_oneway(group_a['Close'], group_b['Close'], group_c['Close'])

# Definir hipótesis nula y alternativa
st.write("Hipótesis nula (Ho): No hay diferencias significativas entre los grupos.")
st.write("Hipótesis alternativa (Ha): Hay al menos una diferencia significativa entre los grupos.")

# Mostrar resultados del ANOVA
st.write(f"Estadística F: {f_statistic:.4f}")
st.write(f"Valor p: {p_value:.4f}")

# Calcular F crítico
alpha = 0.05
df_between = 2  # Grados de libertad entre grupos (número de grupos - 1)
df_within = len(anova_data) - 3  # Grados de libertad dentro de los grupos (total de observaciones - número de grupos)
f_critical = stats.f.ppf(1 - alpha, df_between, df_within)

# Mostrar el valor de F crítico
st.write(f"F crítico (α = {alpha}): {f_critical:.4f}")

# Conclusión del ANOVA
st.subheader("Conclusión del ANOVA")

# Comparar F y F crítico para aceptar o rechazar Ho
if f_statistic > f_critical:
    st.write("Rechazamos la hipótesis nula (Ho).")
    st.write("Esto sugiere que hay una diferencia significativa entre al menos dos de los grupos.")
else:
    st.write("No rechazamos la hipótesis nula (Ho).")
    st.write("Esto sugiere que no hay evidencia suficiente para afirmar que hay diferencias significativas entre los grupos.")

# Gráfico de barras comparando las medias de los tres grupos
st.subheader("Gráfico Comparativo de las Medias de los Tres Grupos")
plt.figure(figsize=(8, 6))
plt.bar(group_means['Grupo'], group_means['Media'], color=['blue', 'green', 'red'])
plt.ylabel("Precio de cierre promedio")
plt.title("Comparación de Medias entre los Grupos A, B y C")
st.pyplot(plt)
