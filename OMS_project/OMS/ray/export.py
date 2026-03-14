import csv
import numpy as np


def export_ray_modes(filename, modes, slab):
    """
    Guarda los modos obtenidos con el modelo de rayos en un archivo CSV.

    Parameters
    ----------
    filename : str
        Nombre del archivo de salida.
    modes : dict
        Diccionario con los modos, formato: {"TE": {m:theta}, "TM": {m:theta}}.
    slab : objeto SymmetricSlabRay
        Objeto que contiene las propiedades del slab (polarización, n_core, k0).
    """

    # Abrir el archivo en modo escritura
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)

        # Escribir la cabecera del archivo CSV
        writer.writerow([
            "mode",
            "polarization",
            "theta(rad)",
            "theta(deg)",
            "neff",
            "beta(1/m)"
        ])

        m = 0  # Contador de modos
        # Iterar sobre los modos en el diccionario
        for modo in modes:
            pol = slab.polarization  # Polarización del modo
            theta = float(modes[modo][0])  # Ángulo theta en radianes
            neff = np.sin(theta) * slab.n_core  # Índice efectivo
            beta = neff * slab.k0  # Constante de propagación

            # Escribir los datos del modo en el archivo CSV
            writer.writerow([
                m,
                pol,
                theta,
                np.degrees(theta),
                neff,
                beta
            ])
            m += 1  # Incrementar el contador de modos