import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
import os



respuestasRuta = r"C:\Users\Ismael\Documents\insti\psico\halo\respuestas.csv"

def import_data(ruta):
    
    datos = pd.read_csv(ruta)
    
    return datos

def valores_imagenes(data, rangoInicio=0):
    personasValue = []
    rangoInicio = rangoInicio*6 if rangoInicio != 0 else 0
    for index in range(rangoInicio, 42, 6):
        persona = data.iloc[:, index: index+6]
        if index != 0:
            persona.columns = map(lambda x: x[:-2], persona.columns) 
        personasValue.append(persona)
    return personasValue


def columnasUnidas(grupo):
    total = grupo[0]

    for persona in grupo[1:]:
        total = pd.concat([total, persona], ignore_index=True)
        #print(total)
    return total

def correlaciones(total):
    return total.corr()

def tabla(data, name):
    df_tabla = data.reset_index()
    df_tabla.columns = [''] + list(data.columns)

    # Crear figura
    fig, ax = plt.subplots(figsize=(19.2, 10.8))
    ax.axis('off')

    # Crear la tabla
    tabla = ax.table(
        cellText=df_tabla.values,
        colLabels=df_tabla.columns,
        cellLoc='center',
        loc='center'
    )

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(18)
    for (i, j), cell in tabla.get_celld().items():
        cell.set_fontsize(20)  # Ajusta el tamaño de la fuente
        cell.set_height(0.1)  # Ajusta la altura de las filas
        cell.set_width(0.1)   # Ajusta el ancho de las columnas

    plt.tight_layout()
    plt.savefig(name)
    plt.close()

def diffCorrelaciones(corr1, corr2, rang1=1, rang2=-1):
    par = [corr1["Belleza"][rang1:rang2].mean(), corr2["Belleza"][rang1:rang2].mean()]
    print(par)
    variacion = (par[1] - par[0]) / (par [0]**2)**0.5 * 100
    return variacion



respuestas = import_data(respuestasRuta)
valorImagenes = valores_imagenes(respuestas.iloc[:, 1:])
totalCols = columnasUnidas(valorImagenes)
print(valorImagenes)
correlacion = correlaciones(totalCols)
#tabla(correlacion.round(4))
valorImagenesClean = valores_imagenes(respuestas.iloc[:, 1:], 3)
totalColsClean = columnasUnidas(valorImagenesClean)
correlacionClean = correlaciones(totalColsClean)
#tabla(correlacionClean.round(4))
#print(correlacionClean)
creciente = round(diffCorrelaciones(correlacion, correlacionClean, 1, 4), 2)
decreciente = round(diffCorrelaciones(correlacion, correlacionClean, 4, correlacion.shape[1]), 2)
print(creciente,decreciente)
print(valorImagenes[6])
correPersona = []
for index, i in enumerate(valorImagenes):
    correPersona.append(correlaciones(i))
    tabla(correlaciones(i).round(4), f"Persona{index}")
print("JJJ")
