import numpy as np
from .root_scalar import RootResult


def bisection(f, bracket, tol=1e-10, max_iter=100):
    """
    Bisection root-finding method.

    Parameters
    ----------
    f : callable
        Function f(x)
    bracket : tuple
        (a, b) with f(a)*f(b) < 0
    tol : float
        Absolute tolerance
    max_iter : int
        Maximum iterations

    Returns
    -------
    RootResult
    """

    a, b = bracket

    fa = f(a)
    fb = f(b)

    # --- Validaciones ---
    if np.isnan(fa) or np.isnan(fb):
        raise ValueError("Function returns NaN at bracket endpoints.")

    if fa * fb > 0:
        raise ValueError("Bisection requires f(a)*f(b) < 0.")

    for iteration in range(1, max_iter + 1):

        c = 0.5 * (a + b)
        fc = f(c)

        if np.isnan(fc):
            raise ValueError("Function returned NaN during iteration.")

        # --- Criterios de parada ---
        if abs(fc) < tol:
            return RootResult(c, True, iteration, method="bisection")

        if abs(b - a) < tol:
            return RootResult(c, True, iteration, method="bisection")

        # --- Actualización del intervalo ---
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    # Si sale del loop → no convergió
    return RootResult(c, False, max_iter, method="bisection")