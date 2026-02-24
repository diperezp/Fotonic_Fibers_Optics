# Importar funciones y módulos necesarios
from ..opticutil.find_roots import find_all_roots
from .simetric_slab import SymmetricSlabRay
import numpy as np

def find_guided_modes_ray(slab):
    """
    Encuentra todos los modos guiados de una losa óptica simétrica.
    
    Parámetros:
        slab: Objeto de losa óptica simétrica
    
    Retorna:
        modes: Diccionario con los modos guiados encontrados
    """
    # Definir el rango angular: desde el ángulo crítico + pequeño offset hasta pi/2
    theta_min = slab.theta_critical() + 1e-6
    theta_max = np.pi/2 - 1e-6

    # Calcular el parámetro F máximo y el número máximo de modos
    Fmax = slab.F(theta_min)
    m_max = int(Fmax // (2*np.pi))

    # Inicializar diccionario para almacenar los modos
    modes = {}

    # Iterar sobre cada número de modo m
    for m in range(m_max + 1):
        # Definir la función característica: F(theta) - m*2*pi = 0
        def f(theta):
            return slab.F(theta) - m*2*np.pi

        # Encontrar todas las raíces de la función en el rango [theta_min, theta_max]
        roots = find_all_roots(f, (theta_min, theta_max))

        # Si se encuentran raíces, almacenarlas en el diccionario
        if roots:
            modes[m] = roots

    # Retornar el diccionario de modos guiados encontrados
    return modes
