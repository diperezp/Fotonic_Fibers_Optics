import numpy as np
from OMS.opticutil.find_roots import find_all_roots

class SymmetricSlabRay:
    """Clase para analizar modos de rayos en una guía de onda de losa simétrica."""

    def __init__(self, n_core, n_clad, n_subs, h, wavelength, polarization='TE'):
        """
        Inicializa los parámetros de la guía de onda simétrica.
        
        Args:
            n_core: Índice de refracción del núcleo
            n_clad: Índice de refracción del revestimiento
            n_subs: Índice de refracción del sustrato
            h: Espesor del núcleo
            wavelength: Longitud de onda
            polarization: Tipo de polarización ('TE' o 'TM')
        """
        self.n_core = n_core
        self.n_clad = n_clad
        self.n_subs = n_subs
        self.h = h
        # Número de onda k0 = 2π/λ
        self.k0 = 2*np.pi / wavelength
        self.polarization = polarization.upper()

    def theta_critical(self):
        """
        Calcula el ángulo crítico de incidencia.
        
        Returns:
            float: Ángulo crítico en radianes
        """
        # Determina el ángulo crítico según el índice de refracción menor
        if(self.n_clad > self.n_subs):
            return np.arcsin(self.n_clad / self.n_core)
        else:
            return np.arcsin(self.n_subs / self.n_core)
    

    def phi_clad(self, theta):
        """
        Calcula el desfase en la región del revestimiento.
        
        Args:
            theta: Ángulo de incidencia en radianes
            
        Returns:
            float: Desfase en el revestimiento
        """
        # Calcula el numerador de la ecuación de desfase
        numerator = np.sqrt(
            self.n_core**2 * np.sin(theta)**2 - self.n_clad**2
        )

        # Calcula el denominador de la ecuación de desfase
        denominator = self.n_core * np.cos(theta)

        # Factor de polarización
        if self.polarization == "TE":
            factor = 1.0

        elif self.polarization == "TM":
            factor = (self.n_core**2 / self.n_clad**2)

        else:
            raise ValueError("Polarization must be 'TE' or 'TM'")

        return np.arctan(factor * numerator / denominator)
    
    def phi_subs(self, theta):
        """
        Calcula el desfase en la región del sustrato.
        
        Args:
            theta: Ángulo de incidencia en radianes
            
        Returns:
            float: Desfase en el sustrato
        """
        # Calcula el numerador de la ecuación de desfase
        numerator = np.sqrt(
            self.n_core**2 * np.sin(theta)**2 - self.n_subs**2
        )

        # Calcula el denominador de la ecuación de desfase
        denominator = self.n_core * np.cos(theta)

        # Factor de polarización
        if self.polarization == "TE":
            factor = 1.0

        elif self.polarization == "TM":
            factor = (self.n_core**2 / self.n_subs**2)

        else:
            raise ValueError("Polarization must be 'TE' or 'TM'")

        return np.arctan(factor * numerator / denominator)

    def F(self, theta):
        """
        Calcula la función característica para encontrar los modos de la guía.
        
        Args:
            theta: Ángulo de incidencia en radianes
            
        Returns:
            float: Valor de la función característica
        """
        # Ecuación de dispersión de la guía de onda simétrica
        return (
            2*self.n_core*self.k0*self.h*np.cos(theta)
            - 2*self.phi_clad(theta)
            - 2*self.phi_subs(theta)
        )
