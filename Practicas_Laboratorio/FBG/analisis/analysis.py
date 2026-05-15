#importamos librerias para el manejor de archivos y directorios
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import tkinter as tk
from tkinter import filedialog
import scienceplots

plt.style.use(['science', 'no-latex'])  # Estilo científico sin LaTeX

mass = [0,46.81,46.69,46.67,47.10,47.13,47.11,47.03,46.87,47.10]

#sumamos progresivamente los valores de la lista mass para obtener una lista de masas acumuladas
mass_acumulada = np.cumsum(mass)
#mostramos la lista de masas acumuladas
print(mass_acumulada)


#inicialmente se le pide al usuario que seleccione el directorio donde se encuentran los archivos .csv
root = tk.Tk()
root.withdraw()
folder_path = filedialog.askdirectory(title="Selecciona el directorio que contiene los archivos .csv")
archivos_csv = [f for f in os.listdir(folder_path)]
print(f"Archivos .csv encontrados: {archivos_csv}")
#se crea una lista vacia para almacenar los dataframes de cada archivo .csv
dataframes = []
#se lee cada archivo .csv y se almacena en la lista de dataframes
for archivo in archivos_csv:
    ruta_archivo = os.path.join(folder_path, archivo)
    df = pd.read_csv(ruta_archivo, skiprows=34)
    dataframes.append(df)
#normalizamos los datos de cada dataframe y aplicamos el filtro de Savitzky-Golay
datos_filtrados = []
for df in dataframes:
    y = df.iloc[:, 1].values
    y_normalizada = (y - np.min(y)) / (np.max(y) - np.min(y))
    y_filtrada = savgol_filter(y_normalizada, window_length=11, polyorder=2)
    datos_filtrados.append(y_filtrada)
x=dataframes[0].iloc[:, 0].values
reflexion_forward = datos_filtrados[0:10]
reflexion_backward = datos_filtrados[10:19]
transmision_forward = datos_filtrados[19:29]
transmision_backward = datos_filtrados[29:len(datos_filtrados)]
#graficamos los datos en un collage de 2 filas y 2 columnas
fig, axs = plt.subplots(2, 2, figsize=(15, 10))
for i in range(min(10, len(reflexion_forward))):
    axs[0, 0].plot(x, reflexion_forward[i], label=f'\u03BB {i} - %.2f g' % mass_acumulada[i])
    title = 'Reflexión Forward'
    axs[0,0].legend(fontsize='x-large')
    axs[0, 0].set_title(title, fontsize=16)
    axs[0, 0].set_xlabel('Longitud de Onda (nm)')
    axs[0, 0].set_ylabel('Potencia (W/W)')
for i in range(min(10, len(reflexion_backward))):
    axs[0, 1].plot(x, reflexion_backward[-i], label=f'\u03BB {i} - %.2f g' % mass_acumulada[len(mass_acumulada)-i-1])
    title = 'Reflexión Backward'
    axs[0, 1].set_title(title, fontsize=16)
    axs[0,1].legend(fontsize='x-large')
    axs[0, 1].set_xlabel('Longitud de Onda (nm)')
    axs[0, 1].set_ylabel('Potencia (W/W)')
for i in range(min(10, len(transmision_forward))):
    axs[1, 0].plot(x, transmision_forward[i], label=f'\u03BB {i} - %.2f g' % mass_acumulada[i])
    title = 'Transmisión Forward'
    axs[1, 0].set_title(title, fontsize=16)
    axs[1, 0].legend(fontsize='x-large')
    axs[1, 0].set_xlabel('Longitud de Onda (nm)')
    axs[1, 0].set_ylabel('Potencia (W/W)')
for i in range(min(10, len(transmision_backward))):
    axs[1, 1].plot(x, transmision_backward[-i], label=f'\u03BB {i} - %.2f g' % mass_acumulada[len(mass_acumulada)-i-1])
    title = 'Transmisión Backward'
    axs[1, 1].set_title(title, fontsize=16)
    axs[1, 1].legend(fontsize='x-large')
    axs[1, 1].set_xlabel('Longitud de Onda (nm)')
    axs[1, 1].set_ylabel('Potencia (W/W)')
#mostramos los primeros 9 dataframes en un trace en un solo plot
# fig=plt.figure(figsize=(10, 6))
# for i in range(min(10, len(dataframes))):
#     x = dataframes[i].iloc[:, 0]
#     y = dataframes[i].iloc[:, 1]
#     y_filtrada = datos_filtrados[i]
#     plt.plot(x, y_filtrada, label=f'\u03BB {i} - %.2f g' % mass_acumulada[i])
plt.legend(fontsize='x-large')
plt.show()


