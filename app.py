# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 17:10:57 2024

@author: jperezr
"""   

import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Proyecto Final", layout="wide")

# Título
#st.title("Proyecto Final")

# Sección de estadísticas para la investigación
st.header("Estadísticas para la Investigación")
#st.write("Aquí puedes incluir información relevante sobre las estadísticas que has utilizado en tu investigación.")

# Sección del proyecto final
st.header("Proyecto Final")
#st.write("Descripción breve del proyecto final y su objetivo.")

# Sección de análisis de precios de acciones de AAPL
st.header("Análisis de Precios de Acciones de Apple Inc., AAPL")
#st.write("Aquí puedes incluir un análisis detallado de los precios de las acciones de AAPL.")

# Información adicional
st.sidebar.header("Información Adicional")
st.sidebar.write("Nombre: Javier Horacio Pérez Ricárdez")
st.sidebar.write("Catedrático: Gabriela Macías Esquivel")
st.sidebar.write("Fecha: Octubre del 2024")

# Despliegue de otras secciones
#st.sidebar.header("Navegación")
#st.sidebar.write("[Sección 1](pages/seccion1.py)")
#st.sidebar.write("[Sección 2](pages/seccion2.py)")
#st.sidebar.write("[Sección 3](pages/seccion3.py)")
#st.sidebar.write("[Sección 4](pages/seccion4.py)")

# Instrucciones para el usuario
#st.write("Navega a través de las secciones en el menú lateral para explorar más sobre el proyecto.")
