class RootResult:
    def __init__(self, root, converged, iterations, method):
        self.root = root
        self.converged = converged
        self.iterations = iterations
        self.method = method

    def __repr__(self):
        status = "converged" if self.converged else "not converged"
        return f"<RootResult root={self.root:.6e}, {status}, iter={self.iterations}>"
def root_scalar(
    f,
    method="brent",
    bracket=None,
    x0=None,
    df=None,
    tol=1e-10,
    max_iter=100
):
    """
    General scalar root finder.
    
    Parameters
    ----------
    f : callable
        Function f(x)
    method : str
        'bisection', 'brent', or 'newton'
    bracket : tuple
        (a, b) interval where f(a)*f(b) < 0
    x0 : float
        Initial guess (for newton)
    df : callable
        Derivative function (required for newton)
    tol : float
        Absolute tolerance
    max_iter : int
        Maximum iterations
    """
    if method == "bisection":
        from .bisection import bisection
        return bisection(f, bracket, tol, max_iter)

    elif method == "brent":
        from .brent import brent
        return brent(f, bracket, tol, max_iter)

    else:
        raise ValueError(f"Unknown method '{method}'")