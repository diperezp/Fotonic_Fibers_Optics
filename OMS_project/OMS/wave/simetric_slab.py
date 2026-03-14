import numpy as np
from OMS.opticutil.find_roots import find_all_roots
class SimetricSlabWave:
    def __init__(self, n_core, n_clad, wavelength, thickness, polarization="TE"):
        """
        Inicializa una guía de onda de slab simétrica.

        Parámetros:
        n_core: Índice de refracción del núcleo.
        n_clad: Índice de refracción del revestimiento.
        wavelength: Longitud de onda de la luz (en las mismas unidades que thickness).
        thickness: Grosor del núcleo.
        polarization: Polarización de la luz ("TE" o "TM").
        """
        self.n_core = n_core
        self.n_clad = n_clad
        self.wavelength = wavelength
        self.h = thickness
        self.polarization = polarization

        self.k0 = 2 * np.pi / self.wavelength
        self.V = self.k0 * (self.h/2) * np.sqrt(self.n_core**2 - self.n_clad**2)

    def TE_even(self, u):
        """
        Calcula la ecuación característica para modos TE pares.

        Parámetros:
        u: Parámetro de modo transversal.

        Retorna:
        Valor de la ecuación característica para el modo TE par.
        """
        w = np.sqrt(self.V**2 - u**2)
        return u * np.tan(u) - w

    def TE_odd(self, u):
        """
        Calcula la ecuación característica para modos TE impares.

        Parámetros:
        u: Parámetro de modo transversal.

        Retorna:
        Valor de la ecuación característica para el modo TE impar.
        """
        w = np.sqrt(self.V**2 - u**2)
        return u/np.tan(u) + w

    def TM_even(self, u):
        """
        Calcula la ecuación característica para modos TM pares.

        Parámetros:
        u: Parámetro de modo transversal.

        Retorna:
        Valor de la ecuación característica para el modo TM par.
        """
        w = np.sqrt(self.V**2 - u**2)
        return (self.n_clad**2 / self.n_core**2) * u * np.tan(u) - w

    def TM_odd(self, u):
        """
        Calcula la ecuación característica para modos TM impares.

        Parámetros:
        u: Parámetro de modo transversal.

        Retorna:
        Valor de la ecuación característica para el modo TM impar.
        """
        w = np.sqrt(self.V**2 - u**2)
        return (self.n_clad**2 / self.n_core**2) * u / np.tan(u) + w

    def find_modes_wave(slab):
        """
        Encuentra los valores de u para los modos soportados por la guía.

        Parámetros:
        slab: Instancia de SimtricSlabWave.

        Retorna:
        Diccionario con listas de raíces para modos pares ('even') e impares ('odd').
        """
        modes = {}
        interval = (1e-6, slab.V-1e-6)
        list=find_all_roots(slab.TE_even, interval)+find_all_roots(slab.TE_odd, interval)
        list.sort()
        for i, u in enumerate(list):
            modes[i] = u        
        return modes

    def u_to_neff(self, u):
        """
        Convierte el parámetro u al índice efectivo del modo.

        Parámetros:
        u: Parámetro de modo transversal.

        Retorna:
        Índice efectivo (n_eff) correspondiente al valor de u.
        """
        beta = np.sqrt(self.k0**2 * self.n_core**2 - (u / self.h)**2)
        return beta / self.k0