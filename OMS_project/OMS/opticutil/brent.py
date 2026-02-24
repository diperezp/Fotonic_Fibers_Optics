import numpy as np
from .root_scalar import RootResult


def brent(f, bracket, tol=1e-10, max_iter=100):
    """
    Implementa el método de Brent para encontrar raíces de funciones.
    
    Args:
        f: Función para la cual encontrar la raíz
        bracket: Tupla (a, b) que contiene un intervalo donde existe una raíz
        tol: Tolerancia de convergencia (por defecto 1e-10)
        max_iter: Número máximo de iteraciones (por defecto 100)
    
    Returns:
        RootResult: Objeto que contiene el resultado de la búsqueda
    """
    # Desempaqueta los extremos del intervalo y evalúa la función en ellos
    a, b = bracket
    fa = f(a)
    fb = f(b)

    # Valida que la función no retorna NaN en los extremos
    if np.isnan(fa) or np.isnan(fb):
        raise ValueError("Function returns NaN at bracket endpoints.")

    # Verifica que la función tiene signos opuestos en los extremos (condición para Brent)
    if fa * fb > 0:
        raise ValueError("Brent requires f(a)*f(b) < 0.")

    # Intercambia a y b para que |f(a)| < |f(b)|
    if abs(fa) < abs(fb):
        a, b = b, a
        fa, fb = fb, fa

    # Inicializa variables auxiliares para el método de Brent
    c = a
    fc = fa
    d = e = b - a

    # Itera hasta encontrar la raíz o alcanzar el máximo de iteraciones
    for iteration in range(1, max_iter + 1):

        # Si fb es cero, encontró exactamente la raíz
        if fb == 0:
            return RootResult(b, True, iteration, method="brent")

        # Intenta interpolación cuadrática inversa si las tres evaluaciones son diferentes
        if fa != fc and fb != fc:
            # Inverse quadratic interpolation
            s = (
                a * fb * fc / ((fa - fb) * (fa - fc)) +
                b * fa * fc / ((fb - fa) * (fb - fc)) +
                c * fa * fb / ((fc - fa) * (fc - fb))
            )
        else:
            # Usa el método de la secante como alternativa
            # Secant method
            s = b - fb * (b - a) / (fb - fa)

        # Evalúa varias condiciones para determinar si acepta la interpolación
        # cond1: Verifica que s esté dentro del intervalo válido
        cond1 = not ((3*a + b)/4 < s < b) if a < b else not (b < s < (3*a + b)/4)
        # cond2 y cond3: Verifica que el paso no sea demasiado grande
        cond2 = e and abs(s - b) >= abs(e) / 2
        cond3 = not e and abs(s - b) >= abs(d) / 2
        # cond4 y cond5: Verifica si ha convergido
        cond4 = e and abs(e) < tol
        cond5 = not e and abs(d) < tol

        # Si alguna condición falla, usa bisección
        if cond1 or cond2 or cond3 or cond4 or cond5:
            s = (a + b) / 2
            e = d = b - a
        else:
            # Actualiza el paso anterior
            e = d
            d = b - s

        # Evalúa la función en el nuevo punto
        fs = f(s)

        # Actualiza el punto anterior c
        c, fc = b, fb

        # Actualiza el intervalo manteniendo la raíz entre a y b
        if fa * fs < 0:
            b, fb = s, fs
        else:
            a, fa = s, fs

        # Asegura que |f(a)| < |f(b)|
        if abs(fa) < abs(fb):
            a, b = b, a
            fa, fb = fb, fa

        # Verifica convergencia: si el intervalo es suficientemente pequeño, retorna
        if abs(b - a) < tol:
            return RootResult(b, True, iteration, method="brent")

    # Si se alcanza el máximo de iteraciones sin convergencia, retorna el mejor estimado
    return RootResult(b, False, max_iter, method="brent")