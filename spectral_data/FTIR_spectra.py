'''
Scripts para visualizar datos de transmitancia - espectrómetro JASCO FT/IR-6X
Autor: Ana
Descripción:
    - Carga datos desde uno o múltiples archivos CSV
    - Extrae metadatos relevantes
    - Genera gráficos combinados o individuales según preferencia
'''
#---------------------Librerias y modulos requeridos-------------------------
import os
import chardet
import pandas as pd
import matplotlib.pyplot as plt

#--------------------------Sección de editables------------------------------
# 📁 Dirección de la carpeta que contiene los archivos csv 📁 :
# ↓↓ Copia la dirección aquí ↓↓ (conservar la r que precede al texto)
carpeta= r"C:\Users\Ana\Documents\MyFolder"

# Modo de visualización: gráfico combinado ("C") o individual ("I")
Modo = "I"

# Título de la o las gráficas
Titulo = ""

#---------------Funciones para generar DataFrames y gráficos------------------
def leer_archivos(carpeta):
    carpeta = carpeta.replace("\\","/")
    # lista de archivos csv contenidos en la carpeta:
    archivos_csv= [_ for _ in os.listdir(carpeta) if _.endswith('.csv')]
    # 📦 lista de tuplas (DataFrame, metadata, indice) 📦 :
    lista_datos = []
    for i, archivo in enumerate(archivos_csv):
        ruta = os.path.join(carpeta, archivo)
        # Codigo para detectar el encoding 🔍
        with open(ruta,"rb") as f:
            tipo = chardet.detect(f.read())
        # 💌 Metadatos 💌 
        with open(ruta, encoding=tipo['encoding']) as f:
            lineas_all = f.readlines()
            lineas = [linea.strip() for linea in lineas_all[:19]]+[linea.strip() for linea in lineas_all[-40:]]
        metadata ={}
        for linea in lineas:
            if "," in linea:
                clave, valor = linea.split(",", 1)
                metadata[clave.strip()]=valor.strip()
        # 📚 DataFrames 📚
        filas_totales = len(lineas_all)
        try:
            df = pd.read_csv(ruta, skiprows=19, nrows=filas_totales-19-40, names = ["wavenumber","transmittance"], encoding=tipo['encoding'], engine='python')
        except Exception as e:
            print(f"⚠️ Error al leer {archivo}: {e}")
        # sección de guardado
        tupla = (df, metadata,i)
        lista_datos.append(tupla)
    return lista_datos

def leyenda(dt):
    print(f" Descripción del conjunto de datos 📄: {dt[1]}")
    et = str(input("Leyenda a mostrar en el gráfico 📈:"))
    return et

def figura(datos, modo, titulo):
    if modo == "C":
        fig, ax = plt.subplots()
        print("Ingrese una etiqueta para cada conjunto de datos:")
        for dato in datos:
            df = dato[0]
            etiqueta = leyenda(dato)
            ax.plot(df["wavenumber"],df["transmittance"], label=etiqueta)
        ax.legend()
        ax.set_xlabel("numero de onda (cm⁻¹)")
        ax.set_ylabel("Transmitancia (%)")
        ax.set_title(titulo)
        return fig
    if modo == "I":
        figuras = []
        for dato in datos:
            df = dato[0]
            fig, ax = plt.subplots()
            ax.plot(df["wavenumber"],df["transmittance"])
            ax.set_xlabel("numero de onda (cm⁻¹)")
            ax.set_ylabel("Tansmitancia (%)")
            ax.set_title(titulo)
            figuras.append(fig)
        return figuras

#------------------------------Ejecución-------------------------------------
datos = leer_archivos(carpeta)
grafica = figura(datos, Modo, Titulo)

# Este comando muestra la  o las gráficas, puede guardar los resultados desde la interfaz
plt.show()

'''
Comentarios adicionales:
- Este script está diseñado para ejecutarse en entornos interactivos como VS Code,
Jupyter Notebook o terminales locales. Si deseas automatizarlo, considera reemplazar
input() por argumentos predefinidos o una configuración externa.
- Si existe algún error en el rango de los datos, revisar las líneas 41 y 50 
para ajustar el número de filas de metadatos.
'''
