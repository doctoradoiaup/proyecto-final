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

# Mostrar todos los datos históricos según las fechas seleccionadas
st.subheader("Datos históricos de AAPL")
st.dataframe(data)  # Mostrar todos los datos

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


# Calcular los percentiles 33 y 66
percentile_33 = np.percentile(data['Close'], 33)
percentile_66 = np.percentile(data['Close'], 66)

# Mostrar los valores de los percentiles 33 y 66
st.write(f"El valor del percentil 33 es: {percentile_33:.2f}")
st.write(f"El valor del percentil 66 es: {percentile_66:.2f}")

def categorize_price(row):
    if row['Close'] < percentile_33:
        return "Bajo"
    elif row['Close'] < percentile_66:
        return "Medio"
    else:
        return "Alto"

data['Precio_Categorizado'] = data.apply(categorize_price, axis=1)

# Mostrar todos los datos categorizados según las fechas seleccionadas
st.write("Precios categorizados según percentiles:")
st.dataframe(data[['Date', 'Close', 'Precio_Categorizado']])  # Mostrar todos los datos categorizados

# c) Análisis con variables múltiples
# c) Análisis de la distribución del volumen en relación con las categorías de precios

# c) Análisis de la distribución del volumen en relación con las categorías de precios

# Categorización de los precios
percentile_33 = np.percentile(data['Close'], 33)
percentile_66 = np.percentile(data['Close'], 66)
data['Precio_Categorizado'] = pd.cut(data['Close'], bins=[-np.inf, percentile_33, percentile_66, np.inf],
                                      labels=['Bajo', 'Medio', 'Alto'])

# Analizando la distribución de volumen por categoría de precio
st.write("Distribución del volumen por categoría de precio:")
plt.figure(figsize=(10, 5))
sns.boxplot(x='Precio_Categorizado', y='Volume', data=data)
plt.title("Distribución de Volumen por Categoría de Precio")
st.pyplot(plt)  # Mostrar la figura
plt.clf()  # Limpiar la figura

# Cálculo de estadísticas del boxplot
stats = data.groupby('Precio_Categorizado')['Volume'].describe()
st.write("Estadísticas del Volumen por Categoría de Precio:")
st.write(stats)

# Explicación y cálculos adicionales
st.write("""
**Cálculos y Procesos:**

1. **Categorización de Precios:**
   - Las categorías de precios se establecen basándose en los percentiles 33 y 66. Esto significa que:
     - Los precios de cierre por debajo del **percentil 33** se clasifican como **Bajo**.
     - Los precios de cierre entre el **percentil 33** y el **percentil 66** se clasifican como **Medio**.
     - Los precios de cierre por encima del **percentil 66** se clasifican como **Alto**.

2. **Cálculo de los Percentiles:**
   - Los percentiles se calculan utilizando la función `np.percentile()`. Por ejemplo:
     ```python
     percentile_33 = np.percentile(data['Close'], 33)
     percentile_66 = np.percentile(data['Close'], 66)
     ```
   - Esto nos permite determinar los valores críticos que dividen el conjunto de datos en las tres categorías.

3. **Boxplot (Diagrama de Caja):**
   - El boxplot proporciona una representación visual de la distribución del volumen de transacciones en cada categoría de precios. Los elementos clave son:
     - **Caja**: Representa el rango intercuartílico (IQR), que muestra dónde se encuentra el 50% central de los datos. 
       - Valor mínimo de la caja (Q1): {:.2f}
       - Valor máximo de la caja (Q3): {:.2f}
     - **Mediana**: La línea dentro de la caja representa la mediana del volumen de acciones negociadas. 
       - Mediana: {:.2f}
     - **Bigotes**: Se extienden hasta el valor mínimo y máximo dentro de 1.5 veces el IQR, indicando el rango general de los datos sin outliers. 
       - Valor mínimo: {:.2f}
       - Valor máximo: {:.2f}
     - **Outliers**: Los puntos fuera de los bigotes son considerados outliers, indicando volúmenes de transacciones inusuales.

4. **Análisis de Resultados:**
   - Al observar el gráfico, se pueden hacer varias inferencias:
     - **Volumen Alto vs Bajo**: Si la caja correspondiente a la categoría **Alto** es significativamente más alta que la de **Bajo**, esto sugiere que los precios más altos están asociados con un mayor volumen de transacciones.
     - **Tendencias en el Volumen**: Cualquier diferencia notable en las alturas de las cajas puede indicar cómo las categorías de precios afectan el volumen de negociación.
     - **Presencia de Outliers**: La cantidad de outliers en cada categoría también es informativa; por ejemplo, un número elevado de outliers en la categoría **Alto** podría indicar eventos extraordinarios que afectan el volumen de negociación.

5. **Conclusión**:
   - Este análisis nos ayuda a entender mejor cómo el volumen de negociación de AAPL varía según las diferentes categorías de precios, lo que es fundamental para la toma de decisiones informadas en el mercado de valores.
""".format(
    stats.loc['Bajo', '25%'],  # Valor mínimo de la caja
    stats.loc['Bajo', '75%'],  # Valor máximo de la caja
    stats.loc['Bajo', '50%'],  # Mediana
    stats.loc['Bajo', 'min'],   # Valor mínimo
    stats.loc['Bajo', 'max']    # Valor máximo
))

# Análisis de la relación entre el volumen y el precio categorizado
st.write("Relación entre el volumen y las categorías de precio:")
plt.figure(figsize=(10, 5))
sns.scatterplot(x='Close', y='Volume', hue='Precio_Categorizado', data=data)
plt.title("Scatterplot de Precio vs Volumen con Categorías")
st.pyplot(plt)  # Mostrar la figura
plt.clf()  # Limpiar la figura

# d) Contar datos por categorías de percentiles
st.subheader("d) Conteo de datos según las categorías de precios")
# Crear un DataFrame con los conteos
conteo_categorias = data['Precio_Categorizado'].value_counts().reset_index()
conteo_categorias.columns = ['Categoría de Precio', 'Conteo']

# Mostrar el DataFrame con los conteos
st.write("Conteo de datos según la categoría de precios:")
st.dataframe(conteo_categorias)

# Conclusiones
st.subheader("Conclusiones")
st.write("""
En este análisis categórico, observamos cómo las diferentes categorías de precios afectan el volumen de transacciones. La categorización del precio ayuda a identificar tendencias del mercado y permite a los inversores comprender mejor el comportamiento de las acciones en diferentes rangos de precios.
""")
