# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 14:06:28 2024

@author: jperezr
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

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

# Calcular probabilidades conjuntas
st.subheader("Probabilidades Conjuntas")

# Definir los rangos de interés para el precio de apertura (X) y el precio de cierre (Y)
x_min, x_max = st.slider('Selecciona el rango de Precio de Apertura (X)', float(data['Open'].min()), float(data['Open'].max()), (float(data['Open'].min()), float(data['Open'].max())))
y_min, y_max = st.slider('Selecciona el rango de Precio de Cierre (Y)', float(data['Close'].min()), float(data['Close'].max()), (float(data['Close'].min()), float(data['Close'].max())))

# i) Probabilidad conjunta P(X en [x_min, x_max] y Y en [y_min, y_max])
prob_joint = np.mean((data['Open'] >= x_min) & (data['Open'] <= x_max) & (data['Close'] >= y_min) & (data['Close'] <= y_max))
st.write(f"P(X en [{x_min:.2f}, {x_max:.2f}] y Y en [{y_min:.2f}, {y_max:.2f}]) = {prob_joint:.4f}")

# ii) Probabilidad de que el precio de cierre sea mayor que el de apertura
prob_close_gt_open = np.mean(data['Close'] > data['Open'])
st.write(f"P(Y > X) = {prob_close_gt_open:.4f}")

# iii) Probabilidad de que el precio de apertura y cierre no coincidan en rangos
x2_min, x2_max = st.slider('Selecciona un segundo rango de Precio de Apertura (X ≠ Y)', float(data['Open'].min()), float(data['Open'].max()), (float(data['Open'].min()), float(data['Open'].max())))
y2_min, y2_max = st.slider('Selecciona un segundo rango de Precio de Cierre (Y ≠ X)', float(data['Close'].min()), float(data['Close'].max()), (float(data['Close'].min()), float(data['Close'].max())))

prob_non_equal_ranges = np.mean((data['Open'] >= x2_min) & (data['Open'] <= x2_max) & (data['Close'] >= y2_min) & (data['Close'] <= y2_max))
st.write(f"P(X en [{x2_min:.2f}, {x2_max:.2f}] y Y en [{y2_min:.2f}, {y2_max:.2f}] ≠) = {prob_non_equal_ranges:.4f}")

# Sección de valores esperados, covarianza y correlación
st.subheader("Valores Esperados, Covarianza y Correlación")

# a) Valores esperados
expected_open = np.mean(data['Open'])
expected_close = np.mean(data['Close'])

st.write(f"Valor Esperado del Precio de Apertura: {expected_open:.2f}")
st.write(f"Valor Esperado del Precio de Cierre: {expected_close:.2f}")

# b) Covarianza
covariance = np.cov(data['Open'], data['Close'])[0][1]
st.write(f"Covarianza entre Precio de Apertura y Precio de Cierre: {covariance:.2f}")

# c) Correlación
correlation = np.corrcoef(data['Open'], data['Close'])[0][1]
st.write(f"Correlación entre Precio de Apertura y Precio de Cierre: {correlation:.2f}")

# Sección de cálculo de E[XY] y Var[XY] usando dobles sumas
st.subheader("Cálculo de E[XY] y Var[XY]")

# Calcular la distribución conjunta usando histogramas bidimensionales
X = data['Open'].dropna().to_numpy()
Y = data['Close'].dropna().to_numpy()

# Crear histograma bidimensional para aproximar la función de masa de probabilidad conjunta
joint_probs, x_edges, y_edges = np.histogram2d(X, Y, bins=20, density=True)

# Anchos de los bins
dx = np.diff(x_edges)
dy = np.diff(y_edges)

# Cálculo de E[XY]
E_XY = 0
for i in range(len(x_edges) - 1):
    for j in range(len(y_edges) - 1):
        E_XY += joint_probs[i, j] * x_edges[i] * y_edges[j] * dx[i] * dy[j]

st.write(f"Valor Esperado E[XY]: {E_XY:.4f}")

# Cálculo de E[(XY)^2]
E_XY2 = 0
for i in range(len(x_edges) - 1):
    for j in range(len(y_edges) - 1):
        E_XY2 += joint_probs[i, j] * (x_edges[i] * y_edges[j]) ** 2 * dx[i] * dy[j]

# Cálculo de la varianza Var(XY)
var_XY = E_XY2 - E_XY ** 2
st.write(f"Varianza Var[XY]: {var_XY:.4f}")

# Mostrar los datos utilizados para el análisis
st.write("Datos de entrada utilizados para el análisis:")
st.dataframe(data)