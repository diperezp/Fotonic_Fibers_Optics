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

    def even(self, u):
        """
        Calcula la ecuación característica para modos TE pares.

        Parámetros:
        u: Parámetro de modo transversal.

        Retorna:
        Valor de la ecuación característica para el modo TE par.
        """
        factor_TM = (self.n_clad**2 / self.n_core**2) if self.polarization == "TM" else 1   
        w = np.sqrt(self.V**2 - u**2)
        return factor_TM * u * np.tan(u) - w
    
    def ecuation_characteristic_odd(self, u):
        """
        Calcula la ecuación característica para modos TE impares.

        Parámetros:
        u: Parámetro de modo transversal.

        Retorna:
        Valor de la ecuación característica para el modo TE impar.
        """
        factor_TM = (self.n_clad**2 / self.n_core**2) if self.polarization == "TM" else 1
        return factor_TM * -u / np.tan(u)
    def ecuation_characteristic_even(self, u):
        """
        Calcula la ecuación característica para modos TE pares.

        Parámetros:
        u: Parámetro de modo transversal.

        Retorna:
        Valor de la ecuación característica para el modo TE par.
        """
        factor_TM = (self.n_clad**2 / self.n_core**2) if self.polarization == "TM" else 1   
        return factor_TM * u * np.tan(u)

    def odd(self, u):
        """
        Calcula la ecuación característica para modos TE impares.

        Parámetros:
        u: Parámetro de modo transversal.

        Retorna:
        Valor de la ecuación característica para el modo TE impar.
        """
        factor_TM = (self.n_clad**2 / self.n_core**2) if self.polarization == "TM" else 1
        w = np.sqrt(self.V**2 - u**2)
        return factor_TM * -u / np.tan(u) - w



    def find_modes_wave(slab):
        """
        Encuentra los valores de u para los modos soportados por la guía.

        Parámetros:
        slab: Instancia de SimtricSlabWave.

        Retorna:
        Diccionario con listas de raíces para modos pares ('even') e impares ('odd').
        """
        even = []
        odd = []

        #dividimo el intervalo por los puntos de inflexion menores entre 0 y V para la tangente
        inflection_points = np.arange(0, slab.V, np.pi/2)
        if inflection_points[-1] != slab.V:
            inflection_points = np.append(inflection_points, slab.V)
        #encontramos las raices para los modos pares e impares
        for i in range(len(inflection_points)-1):
            even+=find_all_roots(slab.even, inflection_points[i:i+2])
        inflection_points = np.arange(0, slab.V, np.pi)
        if inflection_points[-1] != slab.V:
            inflection_points = np.append(inflection_points, slab.V)
        for i in range(len(inflection_points)-1):
            odd+=find_all_roots(slab.odd, inflection_points[i:i+2])
        #unimos las raices en una sola lista
        modes=even+odd
        #eliminamos los modos que sea muy cercanos a los puntos multiplos de pi/2 y pi
        for u in modes[:]:
            if u == 0 or np.isclose(u % (np.pi/2), 0, atol=1e-3) or np.isclose(u % np.pi, 0, atol=1e-3):
                modes.remove(u)
        return sorted(modes)

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