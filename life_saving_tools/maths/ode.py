class ODE:
    """
    A class for solving ODEs using tnumerical methods. Available methods are:
    - Euler's method
    - Euler-modified method
    - Runga-Kutta's second order method
        - Heun's method
        - Midpoint method
        - Ralston's method
    - Runge-Kutta third order method
    - Runge-Kutta fourth order method
    - Runge-Kutta fifth order method
    """

    def __init__(self) -> None:
        pass

    def _euler_(self, f, x0, y0, x, n):
        h = (x - x0) / n
        y_prev = y0
        for i in range(n):
            y_prev = y_prev + f(x0 + i * h, y_prev) * h
        return y_prev

    def _euler_modified_(self, f, x0, y0, x, n):
        h = (x - x0) / n
        y_prev = y0
        for i in range(n):
            y_next = y_prev + h * f(x0 + i * h, y_prev)
            y_prev = (
                y_prev + h * (f(x0 + i * h, y_prev) + f(x0 + (i + 1) * h, y_next)) / 2
            )
        return y_prev

    def _heun_(self, f, x0, y0, x, n):
        h = (x - x0) / n
        y_prev = y0
        for i in range(n):
            k1 = f(x0 + i * h, y_prev)
            k2 = f(x0 + (i + 1) * h, y_prev + h * k1)
            y_prev = y_prev + (k1 + k2) * h / 2
        return y_prev

    def _midpoint_(self, f, x0, y0, x, n):
        h = (x - x0) / n
        y_prev = y0
        for i in range(n):
            k1 = f(x0 + i * h, y_prev)
            k2 = f(x0 + (i + 0.5) * h, y_prev + h * k1 * 0.5)
            y_prev = y_prev + k2 * h
        return y_prev

    def _ralston_(self, f, x0, y0, x, n):
        h = (x - x0) / n
        y_prev = y0
        for i in range(n):
            k1 = f(x0 + i * h, y_prev)
            k2 = f(x0 + (i + 0.75) * h, y_prev + h * k1 * 0.75)
            y_prev = y_prev + (k1 + 2 * k2) * h / 3
        return y_prev

    def _rk3_(self, f, x0, y0, x, n):
        h = (x - x0) / n
        y_prev = y0
        for i in range(n):
            k1 = f(x0 + i * h, y_prev)
            k2 = f(x0 + (i + 0.5) * h, y_prev + h * k1 * 0.5)
            k3 = f(x0 + (i + 1) * h, y_prev - h * k1 + 2 * k2 * h)
            y_prev = y_prev + (k1 + 4 * k2 + k3) * h / 6
        return y_prev

    def _rk4_(self, f, x0, y0, x, n):
        h = (x - x0) / n
        y_prev = y0
        for i in range(n):
            k1 = f(x0 + i * h, y_prev)
            k2 = f(x0 + (i + 0.5) * h, y_prev + h * k1 * 0.5)
            k3 = f(x0 + (i + 0.5) * h, y_prev + h * k2 * 0.5)
            k4 = f(x0 + (i + 1) * h, y_prev + h * k3)
            y_prev = y_prev + (k1 + 2 * k2 + 2 * k3 + k4) * h / 6
        return y_prev

    def _rk5_(self, f, x0, y0, x, n):
        h = (x - x0) / n
        y_prev = y0
        for i in range(n):
            k1 = f(x0 + i * h, y_prev)
            k2 = f(x0 + (i + 0.25) * h, y_prev + h * k1 * 0.25)
            k3 = f(x0 + (i + 0.25) * h, y_prev + (k1 + k2) * h / 8)
            k4 = f(x0 + (i + 0.5) * h, y_prev + (-0.5 * k2 + k3) * h)
            k5 = f(x0 + (i + 0.75) * h, y_prev + 3 * (k1 + 3 * k4) * h / 16)
            k6 = f(
                x0 + (i + 1) * h,
                y_prev + (-3 * k1 + 2 * k2 + 12 * k3 - 12 * k4 + 8 * k5) * h / 7,
            )
            y_prev = y_prev + (7 * k1 + 32 * k3 + 12 * k4 + 32 * k5 + 7 * k6) * h / 90
        return y_prev

    def solve(self, f, x0, y0, x, n, method="rk4"):
        """
        Solves an ODE using numerical method. This

        Parameters
        ----------
        f : function
            The function to be solved.
        x0 : float
            The initial x value.
        y0 : float
            The initial y value.
        x : float
            The final x value.
        n : int
            The number of steps.
        method : str
            The numerical method to be used. Options are:
            - "euler": Euler's method.
            - "euler_modified": Euler-modified method.
            - "heun": Heun's method. (Second order Runge-Kutta method)
            - "midpoint": Midpoint method.(Second order Runge-Kutta method)
            - "ralston": Ralston's method.(Second order Runge-Kutta method)
            - "rk3": Third order Runge-Kutta method.
            - "rk4": Fourth order Runge-Kutta method.
            - "rk5": Fifth order Runge-Kutta method.

        Returns
        -------
        y : float
            The final y value.
        """
        method_dict = {
            "euler": self._euler_,
            "euler_modified": self._euler_modified_,
            "heun": self._heun_,
            "midpoint": self._midpoint_,
            "ralston": self._ralston_,
            "rk3": self._rk3_,
            "rk4": self._rk4_,
            "rk5": self._rk5_,
        }
        if method not in method_dict.keys():
            raise ValueError(
                f"Method {method} is not implemented. Available methods are: {' '.join(method_dict.keys())}"
            )
        return method_dict[method](f, x0, y0, x, n)
