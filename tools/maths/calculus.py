class Derivative:
    """
    A class containing numerical methods for calculating derivatives. The numerical methods are:
    - Forward difference
    - Backward difference
    - Central difference

    """

    def __init__(self, h=1e-5):
        """
        Initialize the class with the function to be differentiated and the point at which to \\
        calculate the derivative.

        Parameters
        ----------
        h : float
            The step size. Default is 1e-5.

        returns
        -------
        None

        """
        self.h = h
        self.methods = {
            "fd": "Forward difference",
            "bd": "Backward difference",
            "cd": "Central difference",
        }
        self.orders = {
            "first": "First order",
            "second": "Second order",
        }
        self.errors = {
            "first": "O(h)",
            "second": "O(h^2)",
            "fourth": "O(h^4)",
        }

    def _fdoh_(self, f, x, h=1e-5):
        return (f(x + h) - f(x)) / (h)

    def _fdoh2_(self, f, x, h=1e-5):
        numerator = -f(x + 2 * h) + 4 * f(x + h) - 3 * f(x)
        denominator = 2 * h
        y_calc = numerator / denominator
        return y_calc

    def _bdoh_(self, f, x, h=1e-5):
        return (f(x) - f(x - h)) / (h)

    def _bdoh2_(self, f, x, h=1e-5):
        numerator = 3 * f(x) - 4 * f(x - h) + f(x - 2 * h)
        denominator = 2 * h
        y_calc = numerator / denominator
        return y_calc

    def _cdoh2_(self, f, x, h=1e-5):
        numerator = f(x + h) - f(x - h)
        denominator = 2 * h
        y_calc = numerator / denominator
        return y_calc

    def _cdoh4_(self, f, x, h=1e-5):
        numerator = -f(x + 2 * h) + 8 * f(x + h) - 8 * f(x - h) + f(x - 2 * h)
        denominator = 12 * h
        y_calc = numerator / denominator
        return y_calc

    def _fdoh2second_(self, f, x, h=1e-5):
        numerator = -f(x + 3 * h) + 4 * f(x + 2 * h) - 5 * f(x + h) + 2 * f(x)
        denominator = h ** 2
        y_calc = numerator / denominator
        return y_calc

    def _bdoh2second_(self, f, x, h=1e-5):
        numerator = 2 * f(x) - 5 * f(x - h) + 4 * f(x - 2 * h) - f(x - 3 * h)
        denominator = h ** 2
        y_calc = numerator / denominator
        return y_calc

    def _cdoh2second_(self, f, x, h=1e-5):
        numerator = f(x + h) - 2 * f(x) + f(x - h)
        denominator = h ** 2
        y_calc = numerator / denominator
        return y_calc

    def _cdoh4second_(self, f, x, h=1e-5):
        numerator = (
            -f(x + 2 * h) + 16 * f(x + h) - 30 * f(x) + 16 * f(x - h) - f(x - 2 * h)
        )
        denominator = 12 * h ** 2
        y_calc = numerator / denominator
        return y_calc

    def derivative(self, f, x, order="first", method="cd", error="fourth", h=1e-5):
        """
        Calculates the derivative of a function `f` at the given point `x`.

        Parameters
        ----------
        f : function
            The function to be differentiated.

        x : float
            The point at which to calculate the derivative.

        order : str
            The order of the derivative. Options are:
            - first : First order
            - second : Second order

        method : str
            The method to use to calculate the derivative. Options are:
            - fd : Forward difference
            - bd : Backward difference
            - cd : Central difference

        error : str
            The order of O(h) while calculating the derivative. Options are:
            - first : First order
            - second : Second order
            - fourth : Fourth order

        h : float
            The step size. Default is 1e-5.

        Returns
        -------
        float
            The derivative of the function at the given point.
        """
        # Checking for valid orders
        if order.lower() not in self.orders.keys():
            print(
                f"Invalid order. Available options are: {' '.join(self.orders.keys())}\nWhich corresponds to {' '.join(self.orders.values())}."
            )
            return None

        # Checking for valid methods
        if method.lower() not in self.methods.keys():
            print(
                f"Invalid method. Available options are: {' '.join(self.methods.keys())}\nWhich corresponds to {' '.join(self.methods.values())}."
            )
            return None

        # Checking for O(h) order errors
        if error.lower() == "first" and method.lower() not in ["fd", "bd"]:
            print(
                f"Only forward and backward difference methods can have an error of O(h)."
            )
            return None

        # Checking for O(h^4) order errors
        if error.lower() == "fourth" and method.lower() != "cd":
            print(f"Only central difference methods can have an error of O(h^4).")
            return None

        methods_dict = {
            "first_fd_first": self._fdoh_,
            "first_fd_second": self._fdoh2_,
            "first_bd_first": self._bdoh_,
            "first_bd_second": self._bdoh2_,
            "first_cd_second": self._cdoh2_,
            "first_cd_fourth": self._cdoh4_,
            "second_bd_second": self._bdoh2second_,
            "second_fd_first": self._fdoh2second_,
            "second_cd_second": self._cdoh2second_,
            "second_cd_fourth": self._cdoh4second_,
        }
        parameter = f"{order.lower()}_{method.lower()}_{error.lower()}"
        try:
            method = methods_dict[parameter]
        except KeyError:
            print(
                f"Invalid method combination. Please specify correct combination of order, method and error."
            )
            return None
        return methods_dict[parameter](f, x, h)


class Integration:
    """
    Class for performing numerical integration. Available methods are:
    - integral as sum
    - trapezoidal rule
    - simpson 1/3 rule
    - simpson 3/8 rule

    """

    def __inti__(self):
        pass

    def _integral_as_sum_(self, f, a=0, b=1, n=100, h=None):
        if n is None and h is not None:
            pass
        elif n is not None and h is None:
            h = (b - a) / n
        elif h is None and n is None:
            print("Please specify either n or h.")
            return None
        sum = 0
        for i in range(n):
            sum += f(a + i * h)
        y_true = sum * h
        return y_true

    def _multi_trapzoid_(self, f, a, b, n):
        h = (b - a) / n
        sum = 0
        sum += f(a)
        sum += f(b)
        for i in range(1, n):
            sum += 2 * f(a + i * h)
        y_true = sum * h / 2
        return y_true

    def _simpson13_(self, f, a, b):
        numerator = f(a) + f(b) + 4 * f((a + b) / 2)
        denominator = 6
        y_true = (b - a) * numerator / denominator
        return y_true

    def _simpson13multi_(self, f, a, b, n):
        h = (b - a) / n
        sum = 0
        sum += f(a)
        sum += f(b)
        for i in range(1, n, 2):
            sum += 4 * f(a + i * h)
        for i in range(2, n, 2):
            sum += 2 * f(a + i * h)
        y_true = sum * h / 3
        return y_true

    def _simpson38_(self, f, a, b):
        h = (b - a) / 3
        numerator = f(a) + 3 * f(a + h) + 3 * f(a + 2 * h) + f(b)
        denominator = 6
        y_true = (b - a) * numerator / denominator

        return y_true

    def _simpson38multi_(self, f, a, b, n):
        h = (b - a) / n
        sum = 0
        sum += f(a)
        sum += f(b)
        for i in range(1, n):
            if n % 3 == 0:
                sum += 2 * f(a + i * h)
                continue
            sum += 3 * f(a + i * h)
        y_true = 3 * h * sum / 8
        return y_true

    def integrate(self, f, a, b, method="simpson13multi", n=100, h=None):
        """
        Calculates definite integral of a function f from limit a to b

        Parameters
        ----------
        f : function
            The function to be integrated.

        a : float
            The lower limit of integration.

        b : float
            The upper limit of integration.

        method : str
            The method to use to calculate the integral. Options are:
            - as_sum : Calculates the integral as a sum of n trapezoids
            - multi_trapzoid : Calculates the integral as a sum of n trapezoids
            - simpson13 : Simpson's 1/3 rule
            - simpson13multi : Simpson's 1/3 rule with multiple subintervals
            - simpson38 : Simpson's 3/8 rule
            - simpson38multi : Simpson's 3/8 rule with multiple subintervals

        n : int
            The number of subintervals. Default is 100.

        h: float
            The step size. Default is None.
            Note that at one time, only one of these is necessary. The function will prefer n over h.

        Returns
        -------
        float
            The integral of the function from limit a to b.
        """
        if n is None and h is not None:
            n = int((b - a) / h)

        methods_dict = {
            "as_sum": self._integral_as_sum_,
            "multi_trapzoid": self._multi_trapzoid_,
            "simpson13": self._simpson13_,
            "simpson13multi": self._simpson13multi_,
            "simpson38": self._simpson38_,
            "simpson38multi": self._simpson38multi_,
        }
        if method not in methods_dict.keys():
            print(
                f"Invalid method. Available options are: {' '.join(methods_dict.keys())}"
            )
            return None
        if "multi" not in method.lower() or method.lower() == "as_sum":
            return methods_dict[method](f, a, b)
        else:
            return methods_dict[method](f, a, b, n)
