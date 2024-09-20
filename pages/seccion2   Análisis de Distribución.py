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
data.reset_index(inplace=True)

# Mostrar datos descargados
st.subheader("Datos Descargados")
st.write(data)



# Sección II.- Análisis de Distribución
st.subheader("Sección II.- Análisis de Distribución")

# a) Intervalos estadísticos basados en una sola muestra
st.subheader("a) Intervalos Estadísticos Basados en una Sola Muestra")

# Definir la muestra
sample_size = 30  # Tamaño de la muestra
sample_data = data['Close'].sample(n=sample_size, random_state=42)  # Tomar una muestra aleatoria
sample_df = pd.DataFrame(sample_data).reset_index(drop=True)

# Calcular media y desviación estándar
#sample_mean = sample_df.mean()[0]
#sample_std = sample_df.std()[0]

## Calcular el intervalo de confianza del 95%
#confidence_level = 0.95
#alpha = 1 - confidence_level
#critical_value = stats.t.ppf(1 - alpha / 2, df=sample_size - 1)
#margin_of_error = critical_value * (sample_std / np.sqrt(sample_size))
#confidence_interval = (sample_mean - margin_of_error, sample_mean + margin_of_error)

## Mostrar resultados
#st.write("Muestra de datos:")
#st.write(sample_df)
#st.write(f"Intervalo de confianza del 95% para la media de la muestra: {confidence_interval}")

# Calcular media y desviación estándar
sample_mean = sample_df.mean()[0]
sample_std = sample_df.std()[0]

# Calcular el intervalo de confianza del 95%
confidence_level = 0.95
alpha = 1 - confidence_level
critical_value = stats.t.ppf(1 - alpha / 2, df=sample_size - 1)
margin_of_error = critical_value * (sample_std / np.sqrt(sample_size))
confidence_interval = (float(sample_mean - margin_of_error), float(sample_mean + margin_of_error))  # Convertir a float

# Mostrar resultados
st.write("Muestra de datos:")
st.write(sample_df)
st.write(f"Intervalo de confianza del 95% para la media de la muestra: {confidence_interval}")




# b) Inferencias basadas en dos muestras
st.subheader("b) Inferencias Basadas en Dos Muestras")

# Definir las dos muestras
sample_size_1 = 30
sample_size_2 = 30

# Muestra 1
sample_1 = data['Close'].sample(n=sample_size_1, random_state=42)
sample_1_df = pd.DataFrame(sample_1).reset_index(drop=True)

# Muestra 2
sample_2 = data['Close'].sample(n=sample_size_2, random_state=43)
sample_2_df = pd.DataFrame(sample_2).reset_index(drop=True)

# Mostrar las muestras
st.write("Muestra 1:")
st.write(sample_1_df)
st.write("Muestra 2:")
st.write(sample_2_df)

# Definir hipótesis nula y alternativa
st.write("Hipótesis nula (Ho): Las medias de las dos muestras son iguales.")
st.write("Hipótesis alternativa (Ha): Las medias de las dos muestras son diferentes.")

# Realizar la prueba t para dos muestras
t_stat, p_value = stats.ttest_ind(sample_1, sample_2)

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
group_a = data['Close'].sample(n=30, random_state=1).reset_index(drop=True)
group_b = data['Close'].sample(n=30, random_state=2).reset_index(drop=True)
group_c = data['Close'].sample(n=30, random_state=3).reset_index(drop=True)

# Crear DataFrames para los grupos A, B y C
df_a = pd.DataFrame({'A': group_a})
df_b = pd.DataFrame({'B': group_b})
df_c = pd.DataFrame({'C': group_c})

# Mostrar los DataFrames en la aplicación
st.subheader("Muestra del Grupo A")
st.dataframe(df_a)

st.subheader("Muestra del Grupo B")
st.dataframe(df_b)

st.subheader("Muestra del Grupo C")
st.dataframe(df_c)

# Tabular los grupos y sus medias
group_means = pd.DataFrame({
    'Grupo': ['A', 'B', 'C'],
    'Media': [group_a.mean(), group_b.mean(), group_c.mean()]
})
st.subheader("Medias de los Grupos")
st.dataframe(group_means)

# Crear un DataFrame combinado para ANOVA
anova_data = pd.DataFrame({
    'Group': ['A'] * 30 + ['B'] * 30 + ['C'] * 30,
    'Values': np.concatenate([group_a, group_b, group_c])
})

# Realizar el ANOVA
f_statistic, p_value = stats.f_oneway(group_a, group_b, group_c)

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
    st.write("Esto sugiere que hay diferencias significativas entre los grupos.")
else:
    st.write("No rechazamos la hipótesis nula (Ho).")
    st.write("Esto sugiere que no hay evidencia suficiente para afirmar que las medias de los grupos son diferentes.")
    
    
    
# d) Análisis de Varianza con Factores Múltiples (ANOVA de dos vías)
st.subheader("d) Análisis de Varianza con Factores Múltiples (ANOVA de Dos Vías)")

# Añadir columnas 'Month' y 'Day_of_week' a los datos para utilizar como factores
data['Month'] = data['Date'].dt.month
data['Day_of_week'] = data['Date'].dt.dayofweek

# Visualizar los datos con las nuevas columnas
st.write("Datos con los factores 'Mes' y 'Día de la Semana':")
st.write(data[['Date', 'Close', 'Month', 'Day_of_week']])

# Realizar el ANOVA de dos vías usando statsmodels
# Definir el modelo utilizando 'Month' y 'Day_of_week' como factores
formula = 'Close ~ C(Month) + C(Day_of_week) + C(Month):C(Day_of_week)'
model = ols(formula, data=data).fit()

# Realizar el ANOVA
anova_table = sm.stats.anova_lm(model, typ=2)

# Calcular F crítico
alpha = 0.05
df_between = 2  # Grados de libertad entre grupos (número de grupos - 1)
df_within = len(data) - anova_table.shape[0]  # Grados de libertad dentro de los grupos

# Calcular F crítico para el ANOVA
f_critical = stats.f.ppf(1 - alpha, df_between, df_within)

# Agregar la columna F crítico a anova_table
anova_table['F crítico'] = f_critical

# Mostrar resultados del ANOVA de dos vías
st.write("Resultados del ANOVA de Dos Vías:")
st.write(anova_table)

# Interpretar los resultados del ANOVA de Dos Vías
st.subheader("Interpretación Detallada del ANOVA de Dos Vías")

# Comparar los valores de F con F crítico
if anova_table.loc['C(Month)', 'F'] > f_critical:
    st.write("El factor 'Mes' tiene un efecto significativo sobre el precio de cierre (F > F crítico).")
else:
    st.write("El factor 'Mes' no tiene un efecto significativo sobre el precio de cierre (F <= F crítico).")

if anova_table.loc['C(Day_of_week)', 'F'] > f_critical:
    st.write("El factor 'Día de la semana' tiene un efecto significativo sobre el precio de cierre (F > F crítico).")
else:
    st.write("El factor 'Día de la semana' no tiene un efecto significativo sobre el precio de cierre (F <= F crítico).")

if anova_table.loc['C(Month):C(Day_of_week)', 'F'] > f_critical:
    st.write("Hay una interacción significativa entre 'Mes' y 'Día de la semana' que afecta al precio de cierre (F > F crítico).")
else:
    st.write("No se observa una interacción significativa entre 'Mes' y 'Día de la semana' que afecte al precio de cierre (F <= F crítico).")

# Comparar los valores de F con F crítico
st.subheader("Comparación de Estadísticas F con F Crítico")
for index, row in anova_table.iterrows():
    if row['F'] > f_critical:
        st.write(f"Rechazamos la hipótesis nula para el efecto {index}. Esto sugiere que hay una diferencia significativa.")
    else:
        st.write(f"No rechazamos la hipótesis nula para el efecto {index}. Esto sugiere que no hay evidencia suficiente para afirmar que hay una diferencia significativa.")

# Resumen final de los resultados
st.subheader("Resumen Final del ANOVA de Dos Vías")
if anova_table['F'].max() > f_critical:
    st.write("Al menos uno de los factores o su interacción tiene un efecto significativo en el precio de cierre.")
else:
    st.write("Ninguno de los factores ni su interacción tienen un efecto significativo en el precio de cierre.")





