# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 17:10:57 2024

@author: jperezr
"""   

import streamlit as st
import base64


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
st.sidebar.write("Catedrática: Gabriela Macías Esquivel")
st.sidebar.write("Fecha: Octubre del 2024")

# Despliegue de otras secciones
#st.sidebar.header("Navegación")
#st.sidebar.write("[Sección 1](pages/seccion1.py)")
#st.sidebar.write("[Sección 2](pages/seccion2.py)")
#st.sidebar.write("[Sección 3](pages/seccion3.py)")
#st.sidebar.write("[Sección 4](pages/seccion4.py)")

# Instrucciones para el usuario
#st.write("Navega a través de las secciones en el menú lateral para explorar más sobre el proyecto.")


# Configuración de la página
#st.set_page_config(page_title="Proyecto Final", layout="wide")

# Título de la aplicación
#st.title("Visor de PDF en Streamlit")

# Ruta del archivo PDF
pdf_file_path = "proyecto-final-2.pdf"  # Cambia esto a la ruta de tu archivo PDF

# Leer el archivo PDF
with open(pdf_file_path, "rb") as pdf_file:
    pdf_bytes = pdf_file.read()

# Ofrecer la descarga del archivo PDF
b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="proyecto-final-2.pdf">Descargar PDF, proyecto final</a>'
st.markdown(href, unsafe_allow_html=True)

##############################

# Configuración de la página
st.set_page_config(page_title="Proyecto Final", layout="wide")

# Sección del proyecto final
st.header("Proyecto Final")

# Ruta del primer archivo PDF
pdf_file_path_1 = "proyecto-final-2.pdf"  # Cambia esto a la ruta de tu primer archivo PDF

# Leer el primer archivo PDF
with open(pdf_file_path_1, "rb") as pdf_file_1:
    pdf_bytes_1 = pdf_file_1.read()

# Ofrecer la descarga del primer archivo PDF
b64_pdf_1 = base64.b64encode(pdf_bytes_1).decode("utf-8")
href_1 = f'<a href="data:application/octet-stream;base64,{b64_pdf_1}" download="proyecto-final-2.pdf">Descargar PDF, Proyecto Final</a>'
st.markdown(href_1, unsafe_allow_html=True)

# Ruta del segundo archivo PDF
pdf_file_path_2 = "presentacion.pdf"  # Cambia esto a la ruta de tu segundo archivo PDF

# Leer el segundo archivo PDF
with open(pdf_file_path_2, "rb") as pdf_file_2:
    pdf_bytes_2 = pdf_file_2.read()

# Ofrecer la descarga del segundo archivo PDF
b64_pdf_2 = base64.b64encode(pdf_bytes_2).decode("utf-8")
href_2 = f'<a href="data:application/octet-stream;base64,{b64_pdf_2}" download="presentacion.pdf">Descargar PDF, presentacion</a>'
st.markdown(href_2, unsafe_allow_html=True)
