from OMS.wave.simetric_slab import SimetricSlabWave
import numpy as np
import matplotlib.pyplot as plt

#Parametros del problema
n_core = 1.5            #indice de refraccion del nucleo
n_cladding = 1.1       #indice de refraccion del recubrimiento
h = 1e-6                #espesor del nucleo
wavelength = 1e-6    #longitud de onda de la luz

#creamos una instancia de la clase SimetricSlabWave
wave_TE = SimetricSlabWave(n_core, n_cladding,wavelength,h, polarization="TE")
wave_TM = SimetricSlabWave(n_core, n_cladding,wavelength,h, polarization="TM")

#llamamos al metodo para encontrar los modos guiados
def modosTM_pares(u):
    return wave_TE.even(u)
def modosTM_impares(u):
    return wave_TE.odd(u)
def modosTE_pares(u):
    return wave_TM.even(u)
def modosTE_impares(u):
    return wave_TM.odd(u)
raices_TE= wave_TE.find_modes_wave()

raices_TM= wave_TM.find_modes_wave()

print("Modos guiados encontrados para TE:")
print(raices_TE)
print("Modos guiados encontrados para TM:")
print(raices_TM)

#graficamos la funcion para encontrar los modos pares
u_values = np.linspace(0, wave_TE.V, 1000)
plt.scatter(raices_TE, [0]*len(raices_TE), color='red', label="Raíces TE")
plt.scatter(raices_TM, [0]*len(raices_TM), color='blue', label="Raíces TM")
plt.plot(u_values, modosTE_pares(u_values), label="TE pares")
plt.plot(u_values, modosTE_impares(u_values), label="TE impares")
plt.plot(u_values, modosTM_pares(u_values), label="TM pares")
plt.plot(u_values, modosTM_impares(u_values), label="TM impares")
plt.axhline(0, color='gray', linestyle='--')
plt.xlabel("u")
plt.ylabel("even(u)")
plt.title("Ecuación característica para modos TE pares")
plt.legend()
plt.ylim(-5*wave_TE.V, 5*wave_TE.V)
plt.grid()
plt.show()

