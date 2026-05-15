import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
import os
from scipy.signal import savgol_filter
import scienceplots

plt.style.use(['science', 'no-latex'])  # Estilo científico sin LaTeX

#direccion del directorio donde se encuentra los archivos .csv
path="C:/Users/diego/Documents/GitHub/Fotonic_Fibers_Optics/Practicas_Laboratorio/FBG/Espectre_Bragg"
#arreglo de masas de cada peso utilizado en la practica
mass = [0,46.81,46.69,46.67,47.10,47.13,47.11,47.03,46.87,47.10]
#arreglo de masas acumuladas
mass_acumulada = np.cumsum(mass)
#arreglo de masas acumuladas invertido
mass_acumulada_invertida = mass_acumulada[::-1]

#abrimos los primeros 10 archivos .csv y los almacenamos extraemos los datos en un np.array y los almacenamos en un arreglo
dataframes = []
def leer_csv(path,init_file,final_file):
    data_trace = []
    for i in range(init_file,final_file):
        prefix = "0" if i < 10 else ""
        file = os.path.join(path,f"W00{prefix}{i}.csv")
        df = pd.read_csv(file, skiprows=34)
        y = df.iloc[:, 1].values
        y_normalizada = (y - np.min(y)) / (np.max(y) - np.min(y))
        y_filtrada = savgol_filter(y_normalizada, window_length=11, polyorder=2)
        data_trace.append((df.iloc[:, 0].values, y_filtrada))
    return data_trace




def cutoff_wavelength(data_trace,arreglo_masas,umbral=0.5,transmission=True):
    trace_cutoff = []
    cutoff_wavelengths = []
    for trace in data_trace:
        #para cada traza, se busca cual es la primera longitu de onda que tiene una potencia aproximada a 0.5
        for i in range(len(trace[1])):
            if transmission:
                if trace[1][i] <= umbral:
                    cutoff_wavelengths.append(trace[0][i])
                    break
            else:
                if trace[1][i] >= umbral:
                    cutoff_wavelengths.append(trace[0][i])
                    break
    trace_cutoff=[arreglo_masas[:len(cutoff_wavelengths)],cutoff_wavelengths]
    return trace_cutoff

#clase de regresion lineal para obtener la pendiente e interseccion de la curva de corte
class LinearRegression:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.n = len(x)
        self.slope = 0
        self.intercept = 0

    def fit(self):
        x_mean = np.mean(self.x)
        y_mean = np.mean(self.y)
        numerator = np.sum((self.x - x_mean) * (self.y - y_mean))
        denominator = np.sum((self.x - x_mean) ** 2)
        self.slope = numerator / denominator
        self.intercept = y_mean - self.slope * x_mean

    def predict(self, x):
        return self.slope * x + self.intercept
    
reflection_cutoff_forward=cutoff_wavelength(leer_csv(path,0,10),mass_acumulada,transmission=False)
reflection_cutoff_backward=cutoff_wavelength(leer_csv(path,10,19),mass_acumulada_invertida,transmission=False)
transmision_cutoff_forward=cutoff_wavelength(leer_csv(path,19,29),mass_acumulada)
transmision_cutoff_backward=cutoff_wavelength(leer_csv(path,29,38),mass_acumulada_invertida)
print("reflexion forward")
print(reflection_cutoff_forward)
print("*****************")
print("reflection backward")
print(reflection_cutoff_backward)
print("******************")
print("Transmition forward")
print(transmision_cutoff_forward)
print("******************")
print("Transmition backward")
print(transmision_cutoff_backward)

regresi_Rforward = LinearRegression(reflection_cutoff_forward[0], reflection_cutoff_forward[1])
regresi_Rforward.fit()
regresi_Rbackward = LinearRegression(reflection_cutoff_backward[0], reflection_cutoff_backward[1])
regresi_Rbackward.fit()
regresi_Tforward = LinearRegression(transmision_cutoff_forward[0], transmision_cutoff_forward[1])
regresi_Tforward.fit()
regresi_Tbackward = LinearRegression(transmision_cutoff_backward[0], transmision_cutoff_backward[1])
regresi_Tbackward.fit()


#graficamos reflection_cutoff_forward
fig=plt.figure(figsize=(10,15))
plt.plot(reflection_cutoff_forward[0],reflection_cutoff_forward[1])
#label=f"\u03BB = {regresi_Rforward.slope:.4f} * masa + {regresi_Rforward.intercept:.2f}"
#plt.plot(reflection_cutoff_forward[0],regresi_Rforward.predict(reflection_cutoff_forward[0]),label="Regresión Lineal: " + label)
plt.plot(reflection_cutoff_forward[0],reflection_cutoff_forward[1],'o',color='b',label="Reflexión forward")
plt.grid("True")
plt.legend(fontsize='x-large')
plt.xlabel("masa [g]")
plt.ylabel(f"\u03BB [nm]")
# plt.show()

#graficamos reflection_cutoff_backward
# fig=plt.figure(figsize=(10,15))
plt.plot(reflection_cutoff_backward[0],reflection_cutoff_backward[1])
# label=f"\u03BB = {regresi_Rforward.slope:.4f} * masa + {regresi_Rbackward.intercept:.2f}"
# plt.plot(reflection_cutoff_backward[0],regresi_Rbackward.predict(reflection_cutoff_backward[0]),label="Regresión Lineal: " + label)
plt.plot(reflection_cutoff_backward[0],reflection_cutoff_backward[1],'o',color='g',label="Reflexión backward")
# plt.grid("True")
plt.legend(fontsize='x-large')
# plt.xlabel("masa [g]")
# plt.ylabel(f"\u03BB [nm]")
plt.show()

# #graficamos transmision_cutoff_forward
# fig=plt.figure(figsize=(10,15))
# plt.plot(transmision_cutoff_forward[0],transmision_cutoff_forward[1])
# #label=f"\u03BB = {regresi_Rforward.slope:.4f} * masa + {regresi_Tforward.intercept:.2f}"
# #plt.plot(transmision_cutoff_forward[0],regresi_Tforward.predict(transmision_cutoff_forward[0]),label="Regresión Lineal: " + label)
# plt.plot(transmision_cutoff_forward[0],transmision_cutoff_forward[1],'o',color='b',label="Transmisión forward")
# plt.grid("True")
# plt.legend(fontsize='x-large')
# plt.xlabel("masa [g]")
# plt.ylabel(f"\u03BB [nm]")

# #graficamos transmision_cutoff_backward
# # fig=plt.figure(figsize=(10,15))
# plt.plot(transmision_cutoff_backward[0],transmision_cutoff_backward[1])
# #label=f"\u03BB = {regresi_Rbackward.slope:.4f} * masa + {regresi_Tbackward.intercept:.2f}"
# #plt.plot(transmision_cutoff_backward[0],regresi_Tbackward.predict(transmision_cutoff_backward[0]),label="Regresión Lineal: " + label)
# plt.plot(transmision_cutoff_backward[0],transmision_cutoff_backward[1],'o',color='g',label="Transmisión backward")
# # plt.grid("True")
# plt.legend(fontsize='x-large')
# # plt.xlabel("masa [g]")
# # plt.ylabel(f"\u03BB [nm]")
# plt.show()

