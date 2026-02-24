import numpy as np
from .root_scalar import root_scalar


def find_all_roots(f, interval, n_samples=1000, tol=1e-10):
    """
    Encuentra todas las raíces de una función en un intervalo dado.
    
    Args:
        f: Función para la cual encontrar raíces
        interval: Tupla (x_min, x_max) que define el intervalo de búsqueda
        n_samples: Número de puntos de muestreo en el intervalo (default: 1000)
        tol: Tolerancia para convergencia y detección de duplicados (default: 1e-10)
    
    Returns:
        Lista ordenada de raíces encontradas
    """
    # Desempacar los límites del intervalo
    x_min, x_max = interval
    # Crear puntos de muestreo equiespaciados en el intervalo
    xs = np.linspace(x_min, x_max, n_samples)

    # Lista para almacenar las raíces encontradas
    roots = []

    # Evaluar la función en el primer punto y inicializar variables
    f_prev = f(xs[0])
    x_prev = xs[0]

    # Iterar sobre los puntos de muestreo
    for x in xs[1:]:
        # Evaluar la función en el punto actual
        f_curr = f(x)

        # ignorar NaNs (valores no numéricos)
        if np.isnan(f_prev) or np.isnan(f_curr):
            x_prev = x
            f_prev = f_curr
            continue

        # Detectar cambio de signo (indica presencia de raíz)
        if f_prev * f_curr < 0:
            try:
                # Usar el método de Brent para encontrar la raíz con precisión
                res = root_scalar(
                    f,
                    method="brent",
                    bracket=(x_prev, x),
                    tol=tol
                )
                # Verificar si el método convergió
                if res.converged:
                    root = res.root

                    # evitar duplicados verificando tolerancia
                    if not any(abs(root - r) < tol for r in roots):
                        roots.append(root)

            except Exception:
                # Ignorar errores y continuar
                pass

        # Actualizar valores para la siguiente iteración
        x_prev = x
        f_prev = f_curr

    # Retornar las raíces ordenadas
    return sorted(roots)