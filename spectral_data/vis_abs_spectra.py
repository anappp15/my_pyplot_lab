'''
Scripts para visualizar datos de absorbancia - espectrofotometro DR-3900
Autor: Ana
Descripción:
    - Carga datos desde uno o múltiples archivos CSV
    - Extrae metadatos relevantes
    - Genera gráficos combinados o individuales según preferencia
'''
#---------------------Librerias y modulos requeridos-------------------------
import os
'''import chardet'''
import pandas as pd
import matplotlib.pyplot as plt

#--------------------------Sección de editables------------------------------
# 📁 Dirección de la carpeta que contiene los archivos csv 📁 :
# ↓↓ Copia la dirección aquí ↓↓ (conservar la r que precede al texto)
carpeta= r"c:\Users\Ana\Documents\MyFolder"

# Modo de visualización: gráfico combinado ("C") o individual ("I")
Modo = "I"

# Título de la o las gráficas
Titulo = "Absorbancia"

#---------------Funciones para generar DataFrames y gráficos------------------
def leer_archivos(carpeta):
    carpeta = carpeta.replace("\\","/")
    # lista de archivos csv contenidos en la carpeta:
    archivos_csv= [_ for _ in os.listdir(carpeta) if _.endswith('.csv')]
    # 📦 lista de tuplas (DataFrame, metadata, indice) 📦 :
    lista_datos = []
    for i, archivo in enumerate(archivos_csv):
        ruta = os.path.join(carpeta, archivo)
        '''
        # Codigo para detectar el encoding 🔍
        with open(ruta,"rb") as f:
            tipo = chardet.detect(f.read())
            print(tipo)
        '''
        # 💌 Metadatos 💌 
        with open(ruta, encoding="UTF-16") as f:
            lineas = [next(f).strip() for _ in range (8)]
        metadata ={}
        for linea in lineas:
            if "," in linea:
                clave, valor = linea.split(",", 1)
                metadata[clave.strip()]=valor.strip()
        # 📚 DataFrames 📚
        try:
            df = pd.read_csv(ruta, skiprows=7, usecols=[0,1], names = ["nm","abs"], encoding="UTF-16")
        except Exception as e:
            print(f"⚠️ Error al leer {archivo}: {e}")
        # sección de limpieza y formato
        df["abs"] = (df["abs"].astype(str).str.replace(",",".", regex = False).str.strip())
        df["abs"] = pd.to_numeric(df["abs"], errors = "coerce")
        df["nm"] = (df["nm"].astype(str).str.replace(",",".", regex = False).str.strip())
        df["nm"] = pd.to_numeric(df["nm"], errors = "coerce")
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
            ax.plot(df["nm"],df["abs"], label=etiqueta)
        ax.legend()
        ax.set_xlabel("Longitud de onda (nm)")
        ax.set_ylabel("Absorbancia")
        ax.set_title(titulo)
        return fig
    if modo == "I":
        figuras = []
        for dato in datos:
            df = dato[0]
            fig, ax = plt.subplots()
            ax.plot(df["nm"],df["abs"])
            ax.set_xlabel("Longitud de onda (nm)")
            ax.set_ylabel("Absorbancia")
            ax.set_title(titulo)
            figuras.append(fig)
        return figuras

#------------------------------Ejecución-------------------------------------
datos = leer_archivos(carpeta)
grafica = figura(datos, Modo, Titulo)

# Este comando muestra la  o las gráficas, puede guardar los resultados desde la interfaz
plt.show() 
