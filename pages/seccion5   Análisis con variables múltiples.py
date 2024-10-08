# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 14:06:28 2024

@author: jperezr
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Título de la aplicación
st.title("Estadística para la investigación")
st.subheader("Proyecto final: Análisis de Precios de Acciones de AAPL")
st.write("Nombre: Javier Horacio Pérez Ricárdez")

# Mantener el estado de las fechas
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

# Sección IV: Análisis con variables múltiples
st.subheader("Sección V.- Análisis con variables múltiples")

# Definir los rangos de interés para el precio de apertura (X) y el precio de cierre (Y) usando dos sliders
x_min, x_max = st.slider('Selecciona el rango de Precio de Apertura (X)', float(data['Open'].min()), float(data['Open'].max()), (float(data['Open'].min()), float(data['Open'].max())))
y_min, y_max = st.slider('Selecciona el rango de Precio de Cierre (Y)', float(data['Close'].min()), float(data['Close'].max()), (float(data['Close'].min()), float(data['Close'].max())))

# Gráfico de dispersión
st.subheader("Gráfico de Dispersión")
fig, ax = plt.subplots()
ax.scatter(data['Open'], data['Close'], alpha=0.5)
ax.axhline(y=y_min, color='r', linestyle='--', label='Límite Inferior Y')
ax.axhline(y=y_max, color='r', linestyle='--', label='Límite Superior Y')
ax.axvline(x=x_min, color='g', linestyle='--', label='Límite Inferior X')
ax.axvline(x=x_max, color='g', linestyle='--', label='Límite Superior X')
ax.set_xlabel("Precio de Apertura (X)")
ax.set_ylabel("Precio de Cierre (Y)")
ax.set_title("Gráfico de Dispersión de Precios")
ax.legend()
st.pyplot(fig)

# Gráfico de densidad (superficie de densidad)
st.subheader("Superficie de Densidad")
fig, ax = plt.subplots()
sns.kdeplot(x=data['Open'], y=data['Close'], fill=True, ax=ax, cmap='Blues', thresh=0, levels=20)

# Actualizar las líneas con los valores de los sliders
ax.axhline(y=y_min, color='r', linestyle='--', label='Límite Inferior Y')
ax.axhline(y=y_max, color='r', linestyle='--', label='Límite Superior Y')
ax.axvline(x=x_min, color='g', linestyle='--', label='Límite Inferior X')
ax.axvline(x=x_max, color='g', linestyle='--', label='Límite Superior X')
ax.set_xlabel("Precio de Apertura (X)")
ax.set_ylabel("Precio de Cierre (Y)")
ax.set_title("Superficie de Densidad de Precios")
ax.legend()
st.pyplot(fig)

# Cálculo de probabilidades
st.subheader("Probabilidades Conjuntas")

# Filtrar los datos según los límites seleccionados en los sliders
filtered_data = data[(data['Open'] >= x_min) & (data['Open'] <= x_max) & (data['Close'] >= y_min) & (data['Close'] <= y_max)]

# i) Probabilidad conjunta P(X en [x_min, x_max] y Y en [y_min, y_max])
prob_joint = np.mean((data['Open'] >= x_min) & (data['Open'] <= x_max) & (data['Close'] >= y_min) & (data['Close'] <= y_max))
st.write(f"P(X en [{x_min:.2f}, {x_max:.2f}] y Y en [{y_min:.2f}, {y_max:.2f}]) = {prob_joint:.4f}")

# ii) Probabilidad de que el precio de cierre sea mayor que el de apertura en los datos filtrados
if not filtered_data.empty:  # Asegurarse de que el DataFrame no esté vacío
    prob_close_gt_open = np.mean(filtered_data['Close'] > filtered_data['Open'])
else:
    prob_close_gt_open = 0.0  # Si no hay datos en el rango seleccionado

st.write(f"P(Y > X) = {prob_close_gt_open:.4f}")

# Sección de valores esperados, covarianza y correlación
st.subheader("Valores Esperados, Covarianza y Correlación")

# i) Cálculo de los valores esperados
expected_open = data['Open'].mean()
expected_close = data['Close'].mean()
st.write(f"Valor Esperado de Precio de Apertura (E[X]) = {expected_open:.2f}")
st.write(f"Valor Esperado de Precio de Cierre (E[Y]) = {expected_close:.2f}")

# ii) Cálculo de la covarianza
covariance = np.cov(data['Open'], data['Close'])[0][1]
st.write(f"Covarianza entre Precio de Apertura y Precio de Cierre = {covariance:.2f}")

# iii) Cálculo de la correlación
correlation = np.corrcoef(data['Open'], data['Close'])[0][1]
st.write(f"Correlación entre Precio de Apertura y Precio de Cierre = {correlation:.2f}")

# Mostrar los datos utilizados para el análisis
st.write("Datos de entrada utilizados para el análisis:")
st.dataframe(data)
