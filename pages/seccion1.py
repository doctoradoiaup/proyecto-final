# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 16:10:04 2024

@author: jperezr
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# Título de la aplicación
st.title("Estadística para la investigación")
st.subheader("Proyecto final: Análisis de Precios de Acciones de Apple Inc., AAPL")
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

# Descripción de datos
st.subheader("Sección I.- Descripción de Datos")
st.write(data.describe())

# Distribuciones probabilísticas
st.subheader("a) Distribuciones Probabilísticas")
sns.histplot(data['Close'], kde=True)
plt.title('Distribución del Precio de Cierre')
st.pyplot()

# Prueba de normalidad
st.subheader("b) Prueba de Normalidad")
k2, p = stats.normaltest(data['Close'].dropna())
st.write(f"Estadístico de prueba: {k2}, p-value: {p}")

# ComboBox para selecciones de transformación
if 'transformation' not in st.session_state:
    st.session_state.transformation = "Ninguna"  # Valor predeterminado

st.session_state.transformation = st.selectbox(
    "Selecciona una transformación para intentar normalizar la distribución:",
    options=["Ninguna", "y = x^2", "y = sqrt(x)", "y = ln(x)", "y = 1/x"],
    index=["Ninguna", "y = x^2", "y = sqrt(x)", "y = ln(x)", "y = 1/x"].index(st.session_state.transformation)
)

# Aplicar transformación seleccionada
if st.session_state.transformation == "y = x^2":
    transformed_data = data['Close'] ** 2
elif st.session_state.transformation == "y = sqrt(x)":
    transformed_data = np.sqrt(data['Close'])
elif st.session_state.transformation == "y = ln(x)":
    transformed_data = np.log(data['Close'].replace(0, np.nan))  # Reemplazar ceros para evitar log(0)
elif st.session_state.transformation == "y = 1/x":
    transformed_data = 1 / data['Close'].replace(0, np.nan)  # Reemplazar ceros para evitar división por cero
else:
    transformed_data = data['Close']

# Visualizar la distribución transformada
st.subheader("c) Distribución Transformada")
sns.histplot(transformed_data.dropna(), kde=True)
plt.title(f'Distribución del Precio de Cierre Transformado: {st.session_state.transformation}')
st.pyplot()

# Nueva prueba de normalidad
k2_transformed, p_transformed = stats.normaltest(transformed_data.dropna())
st.subheader("Nueva Prueba de Normalidad")
st.write(f"Estadístico de prueba (transformado): {k2_transformed}, p-value (transformado): {p_transformed}")
if p_transformed < 0.05:
    st.write("La distribución transformada no es normal")
else:
    st.write("La distribución transformada es normal")
