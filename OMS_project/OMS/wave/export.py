import csv
import numpy as np


def export_wave_modes(filename, modes, slab):
    """
    Guarda los modos obtenidos con el modelo ondulatorio.

    Parameters
    ----------
    filename : str
        archivo de salida
    modes : dict
        {"TE_even":[u], "TE_odd":[u], "TM_even":[u], "TM_odd":[u]}
    slab : objeto SymmetricSlabWave
    """

    with open(filename, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "mode",
            "polarization",
            "u",
            "neff",
            "beta(1/um)"
        ])
        m=0
        for modo in modes:
            pol= slab.polarization
            w=float(modes[modo])
            beta=np.sqrt((slab.n_core*slab.k0)**2 - (2*w/slab.h)**2)*1e-6
            neff=beta/slab.k0

            writer.writerow([
                m,
                pol,
                w,
                neff,
                beta
            ])
            m += 1



