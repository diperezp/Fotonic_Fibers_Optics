from OMS.wave.simetric_slab import SimetricSlabWave
import numpy as np
from OMS.analysis.field import field_wave_guide



#Condiciones del problema
n_core = 1.5            #indice de refraccion del nucleo
n_cladding = 1.1       #indice de refraccion del recubrimiento
h = 1e-6                #espesor del nucleo
wavelength = 1e-6    #longitud de onda de la luz

#creamos una instancia de la clase SimetricSlabWave
wave_TE = SimetricSlabWave(n_core, n_cladding,wavelength,h, polarization="TE")



#creamos una instancia de la clase field_wave_guide
field = field_wave_guide(wave_TE)

field.calculate_fields_1D()

campo_E = field.E

print(campo_E.shape)
