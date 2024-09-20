# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 17:20:37 2024

@author: jperezr
"""

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

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

# Sección IV: Análisis de datos categóricos
st.subheader("Sección IV.- Análisis de datos categóricos: Precios de Acciones de AAPL")

# Mostrar los primeros datos
st.subheader("Datos históricos de AAPL")
st.dataframe(data.head())

# a) Identificación de variables
st.subheader("a) Identificación de Variables")
st.write("En este análisis, utilizamos las siguientes variables financieras de AAPL para evaluar el comportamiento del mercado:")
st.markdown("""
- **Fecha**: La fecha de la observación.
- **Open**: El precio de apertura de la acción.
- **High**: El precio más alto de la acción en el día.
- **Low**: El precio más bajo de la acción en el día.
- **Close**: El precio de cierre de la acción.
- **Volume**: El volumen total de acciones negociadas.
""")

# b) Diseño de experimentos
st.subheader("b) Diseño de Experimentos")
st.write("""
Para analizar la variabilidad del precio de las acciones de AAPL, definimos las siguientes categorías basadas en el rango de precios:
- **Bajo**: Si el precio de cierre es menor al percentil 33.
- **Medio**: Si el precio de cierre está entre el percentil 33 y 66.
- **Alto**: Si el precio de cierre está por encima del percentil 66.
""")

# Crear una nueva columna categórica en función de los percentiles
percentile_33 = np.percentile(data['Close'], 33)
percentile_66 = np.percentile(data['Close'], 66)

def categorize_price(row):
    if row['Close'] < percentile_33:
        return "Bajo"
    elif row['Close'] < percentile_66:
        return "Medio"
    else:
        return "Alto"

data['Precio_Categorizado'] = data.apply(categorize_price, axis=1)

# Mostrar el DataFrame con la nueva columna
st.write("Precios categorizados según percentiles:")
st.dataframe(data[['Date', 'Close', 'Precio_Categorizado']].head())

# c) Análisis con variables múltiples
st.subheader("c) Análisis con Variables Múltiples")
st.write("Realizamos un análisis cruzado entre las variables categorizadas y otras variables financieras.")

# Analizando la distribución de volumen por categoría de precio
st.write("Distribución del volumen por categoría de precio:")
plt.figure(figsize=(10, 5))
sns.boxplot(x='Precio_Categorizado', y='Volume', data=data)
plt.title("Distribución de Volumen por Categoría de Precio")
st.pyplot(plt)  # Mostrar la figura
plt.clf()  # Limpiar la figura

# Análisis de la relación entre el volumen y el precio categorizado
st.write("Relación entre el volumen y las categorías de precio:")
plt.figure(figsize=(10, 5))
sns.scatterplot(x='Close', y='Volume', hue='Precio_Categorizado', data=data)
plt.title("Scatterplot de Precio vs Volumen con Categorías")
st.pyplot(plt)  # Mostrar la figura
plt.clf()  # Limpiar la figura

# Conclusiones
st.subheader("Conclusiones")
st.write("""
En este análisis categórico, observamos cómo las diferentes categorías de precios afectan el volumen de transacciones. La categorización del precio ayuda a identificar tendencias del mercado y permite a los inversores comprender mejor el comportamiento de las acciones en diferentes rangos de precios.
""")