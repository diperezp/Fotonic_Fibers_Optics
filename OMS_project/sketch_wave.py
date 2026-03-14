#importamos la librerias a utilizar
import numpy as np
from OMS.wave.simetric_slab import SimetricSlabWave
from OMS.wave.export import export_wave_modes

#definimos los parametros del problema
n_core = 1.5            #indice de refraccion del nucleo
n_cladding = 1.1       #indice de refraccion del recubrimiento
h = 1e-6                #espesor del nucleo
wavelength = 1e-6    #longitud de onda de la luz

#creamos una instancia de la clase SimetricSlabWave
wave_TE = SimetricSlabWave(n_core, n_cladding,wavelength,h, polarization="TE")



#calculamos los modos guiados
modes_TE = wave_TE.find_modes_wave()
print("Modos guiados encontrados para TE:")
print(modes_TE)

export_wave_modes("modos_wave_TE.csv", modes_TE, wave_TE)

#creamos una instancia de la clase SimetricSlabWave para polarizacion TM
wave_TM = SimetricSlabWave(n_core, n_cladding,wavelength,h, polarization="TM")
modes_TM = wave_TM.find_modes_wave()
print("Modos guiados encontrados para TM:")
print(modes_TM)
export_wave_modes("modos_wave_TM.csv", modes_TM, wave_TM)
