# Importar librerías necesarias
import numpy as np  # No se utiliza en este script
from OMS.ray.simetric_slab import SymmetricSlabRay
from OMS.ray.solver import find_guided_modes_ray

#definir parámetros comunes
n_core = 1.5      # Índice de refracción del núcleo
n_clad = 1.45       # Índice de refracción del revestimiento
n_subs = 1.45    # Índice de refracción del sustrato
h = 1e-6          # Espesor de la losa en metros
wavelength = 1e-6 # Longitud de onda en metros


# Crear una losa simétrica con polarización TE
slab_TE = SymmetricSlabRay(
    n_core=n_core,      # Índice de refracción del núcleo
    n_clad=n_clad,        # Índice de refracción del revestimiento
    n_subs=n_subs,        # Índice de refracción del sustrato
    h=h,          # Espesor de la losa en metros
    wavelength=wavelength, # Longitud de onda en metros
    polarization="TE" # Polarización transversal eléctrica
)

# Encontrar los modos guiados para polarización TE
modes = find_guided_modes_ray(slab_TE)
print("Modos guiados encontrados:")
for m, thetas in modes.items():
    print(f"Modo m={m}:")
    for theta in thetas:
        print(f"  θ = {theta*180/np.pi:.6f}°, n_eff = {np.sin(theta)*slab_TE.n_core:.6f}")

# Crear una losa simétrica con polarización TM
slab_TM = SymmetricSlabRay(
    n_core=n_core,      # Índice de refracción del núcleo
    n_clad=n_clad,        # Índice de refracción del revestimiento
    n_subs=n_subs,        # Índice de refracción del sustrato
    h=h,          # Espesor de la losa en metros
    wavelength=wavelength, # Longitud de onda en metros
    polarization="TM" # Polarización transversal magnética
)

# Encontrar los modos guiados para polarización TM
modes_TM = find_guided_modes_ray(slab_TM)
print("\nModos guiados encontrados para TM:")
for m, thetas in modes_TM.items():
    print(f"Modo m={m}:")
    for theta in thetas:
        print(f"  θ = {theta*180/np.pi:.6f}°, n_eff = {np.sin(theta)*slab_TM.n_core:.6f}")
