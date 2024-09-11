# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 16:47:34 2024

@author: jperezr
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.formula.api import ols

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

# Sección III.- Correlación de Datos
st.subheader("Sección III.- Correlación de Datos")

# a) Regresión lineal simple y correlación
st.subheader("a) Regresión Lineal Simple y Correlación")

# Supongamos que queremos predecir el precio de cierre basado en el volumen
if 'Volume' in data.columns:
    # Calcular la correlación
    correlation = data['Close'].corr(data['Volume'])
    st.write(f"Correlación entre Precio de Cierre y Volumen: {correlation}")

    # Ajustar el modelo de regresión lineal simple
    model_simple = ols('Close ~ Volume', data=data).fit()
    predictions_simple = model_simple.predict(data['Volume'])

    # Extraer coeficientes
    beta_0 = model_simple.params['Intercept']
    beta_1 = model_simple.params['Volume']
    
    # Mostrar la ecuación de la recta en LaTeX
    st.latex(r'''
        \text{Close} = %.2f + %.2f \cdot \text{Volume}
        ''' % (beta_0, beta_1))

    # Crear una figura explícitamente para evitar errores
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(data['Volume'], data['Close'], color='blue', label='Datos Reales')
    ax.plot(data['Volume'], predictions_simple, color='red', label='Predicción', linewidth=2)
    ax.set_title('Regresión Lineal Simple: Precio de Cierre vs Volumen')
    ax.set_xlabel('Volumen')
    ax.set_ylabel('Precio de Cierre')
    ax.legend()
    
    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)

    # Resumen del modelo
    st.write("Resumen del Modelo de Regresión Lineal Simple:")
    st.write(model_simple.summary())
else:
    st.write("No se dispone de la columna 'Volume' para el análisis de regresión lineal simple.")

# b) Regresión no lineal y múltiple
st.subheader("b) Regresión No Lineal y Múltiple")

# Asumiendo que queremos usar 'Close' y 'Volume' para hacer una regresión múltiple
if 'Volume' in data.columns:
    # Crear una nueva variable para una regresión no lineal, como el logaritmo del volumen
    data['Log_Volume'] = np.log(data['Volume'].replace(0, np.nan))

    # Ajustar el modelo de regresión múltiple
    model_multiple = ols('Close ~ Volume + Log_Volume', data=data).fit()
    predictions_multiple = model_multiple.predict(data[['Volume', 'Log_Volume']])

    # Extraer coeficientes
    beta_0_multiple = model_multiple.params['Intercept']
    beta_1_multiple = model_multiple.params['Volume']
    beta_2_multiple = model_multiple.params['Log_Volume']

    # Mostrar la ecuación del modelo múltiple en LaTeX
    st.latex(r'''
        \text{Close} = %.2f + %.2f \cdot \text{Volume} + %.2f \cdot \log(\text{Volume})
        ''' % (beta_0_multiple, beta_1_multiple, beta_2_multiple))

    # Crear una figura explícita para evitar errores
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(data['Volume'], data['Close'], color='blue', label='Datos Reales')
    ax.scatter(data['Volume'], predictions_multiple, color='green', label='Predicción Múltiple', marker='x')
    ax.set_title('Regresión Múltiple: Precio de Cierre vs Volumen y Log(Volumen)')
    ax.set_xlabel('Volumen')
    ax.set_ylabel('Precio de Cierre')
    ax.legend()
    
    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)

    # Resumen del modelo
    st.write("Resumen del Modelo de Regresión Múltiple:")
    st.write(model_multiple.summary())
else:
    st.write("No se dispone de la columna 'Volume' para el análisis de regresión múltiple.")
