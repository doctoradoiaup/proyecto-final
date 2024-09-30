# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 12:33:48 2024

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
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Título de la aplicación
st.title("Estadística para la investigación")
st.subheader("Proyecto final: Análisis de Precios de Acciones de AAPL")
st.write("Nombre: Javier Horacio Pérez Ricárdez")

st.subheader("Sección VI.- Análisis de Precios de Acciones de AAPL usando ANOVA y LSD, 2 Factores, más de dos grupos y varias muestras por grupo")

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

# Función para seleccionar fechas y filtrar datos
def seleccionar_muestras(grupo):
    st.header(f"Seleccionar Fechas para {grupo}")
    sample_date_start = st.date_input(f"Fecha de inicio para {grupo}", value=pd.to_datetime("2020-02-01").date())
    sample_date_end = st.date_input(f"Fecha de fin para {grupo}", value=pd.to_datetime("2020-04-01").date())

    # Filtrar los datos de AAPL para el grupo
    grupo_data = data[(data['Date'] >= pd.to_datetime(sample_date_start)) & (data['Date'] <= pd.to_datetime(sample_date_end))][['Date', 'Close']].reset_index(drop=True)

    # Mostrar DataFrame para el grupo
    st.subheader(f"Muestra del {grupo} (Precios de AAPL entre las fechas seleccionadas)")
    if not grupo_data.empty:
        st.dataframe(grupo_data)
    else:
        st.write(f"No hay datos para {grupo} en el rango seleccionado.")
    return grupo_data

# Seleccionar muestras para los grupos
grupo_a = seleccionar_muestras("Grupo A")
grupo_b = seleccionar_muestras("Grupo B")
grupo_c = seleccionar_muestras("Grupo C")

# Realizar el análisis solo si los grupos tienen datos
if not grupo_a.empty and not grupo_b.empty and not grupo_c.empty:
    # Preparar los datos para ANOVA
    anova_data = pd.DataFrame({
        'Grupo': ['A'] * len(grupo_a) + ['B'] * len(grupo_b) + ['C'] * len(grupo_c),
        'Valores': np.concatenate([grupo_a['Close'], grupo_b['Close'], grupo_c['Close']])
    })

    # Realizar ANOVA
    anova_model = ols('Valores ~ Grupo', data=anova_data).fit()
    anova_table = sm.stats.anova_lm(anova_model, typ=2)

    # Mostrar resultados del ANOVA
    st.subheader("Resultados del ANOVA")
    st.write(anova_table)

    # Hipótesis nula y alternativa
    st.write("**Hipótesis Nula (H0)**: No hay diferencias significativas en los precios de acciones entre los grupos.")
    st.write("**Hipótesis Alternativa (H1)**: Hay diferencias significativas en los precios de acciones entre los grupos.")

    # Calcular LSD
    n_a = len(grupo_a)
    n_b = len(grupo_b)
    n_c = len(grupo_c)

    # Varianza combinada
    var_a = grupo_a['Close'].var(ddof=1)
    var_b = grupo_b['Close'].var(ddof=1)
    var_c = grupo_c['Close'].var(ddof=1)
    
    var_comb = ( (n_a - 1) * var_a + (n_b - 1) * var_b + (n_c - 1) * var_c ) / (n_a + n_b + n_c - 3)

    # Grados de libertad
    df = n_a + n_b + n_c - 3
    
    # Valor crítico t
    alpha = 0.05
    t_critical = stats.t.ppf(1 - alpha / 2, df)

    # Calcular LSD
    lsd = t_critical * np.sqrt(2 * var_comb / n_a)  # Suponiendo n_a = n_b = n_c

    # Realizar la prueba LSD usando Tukey
    tukey_results = pairwise_tukeyhsd(anova_data['Valores'], anova_data['Grupo'])
    
    # Mostrar resultados de la prueba LSD
    st.subheader("Resultados de la Prueba LSD")
    st.write(tukey_results)

    # Gráfico de barras para las diferencias entre medias
    st.subheader("Gráfico de Diferencias entre Medias")
    fig, ax = plt.subplots()

    # Crear gráfico de barras
    diferencias = [
        np.abs(grupo_a['Close'].mean() - grupo_b['Close'].mean()),
        np.abs(grupo_a['Close'].mean() - grupo_c['Close'].mean()),
        np.abs(grupo_b['Close'].mean() - grupo_c['Close'].mean())
    ]
    grupos = ['A vs B', 'A vs C', 'B vs C']
    
    colores = ['green' if diferencia > lsd else 'red' for diferencia in diferencias]

    ax.bar(grupos, diferencias, color=colores)
    ax.set_ylabel('Diferencia de Medias')
    ax.set_title('Comparación de Diferencias entre Medias (Significativa en verde, No significativa en rojo)')

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

    # Conclusión de la prueba
    st.subheader("Conclusión de la Prueba")
    for i, grupo_pair in enumerate(grupos):
        # Mostrar el valor de LSD
        st.write(f"**Valor de LSD:** {lsd:.4f} para {grupo_pair}")
        
        if diferencias[i] > lsd:
            st.write(f"La diferencia entre {grupo_pair} es significativa, se rechaza la hipótesis nula.")
        else:
            st.write(f"La diferencia entre {grupo_pair} no es significativa, se acepta la hipótesis nula.")

else:
    st.write("Por favor, selecciona fechas válidas para todos los grupos para realizar el análisis ANOVA.")
