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

#llamamos al metodo para encontrar los modos guiados
def modosTM_pares(u):
    return wave_TE.TM_even(u)
def modosTM_impares(u):
    return wave_TE.TM_odd(u)
def modosTE_pares(u):
    return wave_TE.TE_even(u)
def modosTE_impares(u):
    return wave_TE.TE_odd(u)

#graficamos la funcion para encontrar los modos pares
u_values = np.linspace(0, 4, 1000)
plt.plot(u_values, modosTE_pares(u_values), label="TE pares")
plt.plot(u_values, modosTE_impares(u_values), label="TE impares")
plt.plot(u_values, modosTM_pares(u_values), label="TM pares")
plt.plot(u_values, modosTM_impares(u_values), label="TM impares")
plt.axhline(0, color='gray', linestyle='--')
plt.xlabel("u")
plt.ylabel("TE_even(u)")
plt.title("Ecuación característica para modos TE pares")
plt.legend()
plt.ylim(0, 4)
plt.grid()
plt.show()

