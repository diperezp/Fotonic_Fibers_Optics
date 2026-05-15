#importamos la librerias necesarias para el funcionamiento del programa
import numpy as np
import matplotlib.pyplot as plt
#libreria para el manejo de archivos
import os
#libreria para el manejo de datos en formato csv
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from scipy.signal import savgol_filter

#funcion de filtro IRR de primer orden
def filtro_irr_1er_orden(x,alfa):
    y = np.zeros(len(x))
    y[0] = x[0]
    for i in range(1, len(x)):
        y[i] = alfa * x[i] + (1 - alfa) * y[i-1]
    return y
#creamos una ventana de dialogo para seleccionar la carpeta donde se encuentran los archivos csv
root = tk.Tk()
root.withdraw()
carpeta = filedialog.askdirectory(title="Selecciona la carpeta donde se encuentran los archivos csv")
#obtenemos la lista de archivos csv en la carpeta seleccionada
archivos_csv = [f for f in os.listdir(carpeta)]
print(f"Archivos csv encontrados: {archivos_csv}")
#leemos todos los archivos csv y los guardamos en una lista de dataframes de pandas
dataframes = []
for archivo in archivos_csv:
    ruta_archivo = os.path.join(carpeta, archivo)
    df = pd.read_csv(ruta_archivo, skiprows=34)
    dataframes.append(df)
#mostramos un resumen de los dataframes leidos
for i, df in enumerate(dataframes):
    print(f"Archivo {i+1}:")
    print(df.head())
    print("\n")
#aplicamos el filtro de Savitzky-Golay a los datos de la segunda columna de cada dataframe y los guardamos en una lista
datos_filtrados = []
for df in dataframes:
    y = df.iloc[:, 1].values
    y_filtrada = savgol_filter(y, window_length=11, polyorder=2)
    datos_filtrados.append(y_filtrada)
#Mostramos los graficos en un collage de 3 filas y 7 columnas
fig, axs = plt.subplots(3, 7, figsize=(20, 10))
for i in range(3):
    for j in range(7):
        index = i * 7 + j
        if index < len(dataframes):
            x = dataframes[index].iloc[:, 0]
            y = dataframes[index].iloc[:, 1]
            y_filtrada = datos_filtrados[index]
            axs[i, j].plot(x, y, label='Datos Originales')
            axs[i, j].set_title(f'{archivos_csv[index]}')
            max_y = 0
            axs[i, j].set_ylim(-100, max_y)
            axs[i, j].legend()
plt.tight_layout()
plt.show()




