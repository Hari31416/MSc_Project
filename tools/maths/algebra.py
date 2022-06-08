import numpy as np
import matplotlib.pyplot as plt
from .calculus import Derivative


class CurveFitting:
    """
    A class to implement mth order polynomial regression using the least squares method.

    Use the `fit` method to fit the model. Then predict the Y values given X values using\\
    the `predict` method.

    """

    def __init__(self) -> None:
        self.beta = None
        self.stats = None

    def fit(self, X, Y, order=3, plot=False, stats=True):
        """
        Polynomial regression of order m using least squares method.

        Parameters
        ----------
        X : array_like
            Independent variable.
        Y : array_like
            Dependent variable.
        order : int, optional
            Order of the polynomial. Default is 3.
        plot : bool, optional
            If True, plot the regression line. Default is True.
        statistics : bool, optional
            If True, return the statistics. Default is True.

        Returns
        -------
        beta : array_like
            Coefficients of the polynomial regression model.
        stats : dict
            Statistics of the polynomial regression model.
            `r2` : square of correlation coefficient
            `syx` : standard error of the estimate
        """
        self.n = len(X)
        Xis = np.zeros(2 * order + 1)
        Yis = np.zeros(order + 1)
        for i in range(0, 2 * order + 1):
            if i == 0:
                Xis[i] = self.n
                continue
            xi = np.sum(X ** i)
            Xis[i] = xi

        for i in range(1, order + 2):
            yi = np.sum(Y * (X ** (i - 1)))
            Yis[i - 1] = yi
        A = np.zeros((order + 1, order + 1))
        for i in range(0, order + 1):
            A[i] = Xis[i : i + order + 1]
        beta = np.linalg.solve(A, Yis)
        self.beta = beta

        if plot:
            X_l = np.linspace(np.min(X) - np.std(X), np.max(X) + np.std(X), 100)

            def predict(X_l):
                Y_l = 0
                for i in range(0, order + 1):
                    Y_l += beta[i] * X_l ** i
                return Y_l

            Y_l = predict(X_l)
            plt.figure(figsize=(10, 8))
            plt.scatter(X, Y)
            plt.plot(X_l, Y_l, "r")
            plt.xlim(np.min(X) - np.std(X), np.max(X) + np.std(X))
            plt.ylim(np.min(Y) - np.std(Y), np.max(Y) + np.std(Y))
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.show()

        if stats:
            ymean = np.mean(Y)
            y_pred = self.predict(X)
            Sr = np.sum((Y - y_pred) ** 2)
            SYX = np.sqrt(Sr / (self.n - order - 1))
            # r2
            r2 = (np.sum((Y - ymean) ** 2) - Sr) / (np.sum((Y - ymean) ** 2))
            stats = {"r2": r2, "syx": SYX}
            self.stats = stats
            return beta, stats
        else:
            return beta

    def predict(self, X_l):
        """
        Predict the Y values given X values.

        Parameters
        ----------
        X_l : array_like
            Independent variable.

        Returns
        -------
        Y_l : array_like
            Predicted Y values.
        """
        Y_l = np.zeros(len(X_l))
        for i in range(0, len(self.beta)):
            Y_l += self.beta[i] * X_l ** i
        return Y_l


class RootFinding:
    """
    A class for finding root of an algebraic equation. Available methods are:
    - bisection
    - newton
    - secant
    """

    def __init__(self) -> None:
        self.root = None

    def _bisection_(self, f, a, b, tol=1e-6, maxiter=100):
        """
        Finds root of an equation using the bisection rule.

        Parameters
        ----------
        f : function
            Function to find the root of.
        a : float
            Lower bound of the interval.
        b : float
            Upper bound of the interval.
        tol : float, optional
            Tolerance. Default is 1e-6.
        maxiter : int, optional
            Maximum number of iterations. Default is 100.

        Returns
        -------
        root : float
            Root of the equation.
        """
        for _ in range(maxiter):
            root = (a + b) / 2
            multiple = f(a) * f(root)
            if np.abs(multiple) < tol:
                return root
            if multiple > 0:
                a = root
            elif multiple < 0:
                b = root
        print("Max iterations reached")
        return root

    def _newton_(self, f, x0, x1=None, tol=1e-6, maxiter=100):
        """
        Finds root of an equation using the Newton's method.

        Parameters
        ----------
        f : function
            Function to find the root of.
        x0 : float
            Initial guess.
        tol : float, optional
            Tolerance. Default is 1e-6.
        maxiter : int, optional
            Maximum number of iterations. Default is 100.

        Returns
        -------
        root : float
            Root of the equation.
        """
        d = Derivative()
        for _ in range(maxiter):
            x = x0 - f(x0) / d.derivative(f, x0)
            if np.abs(x - x0) < tol:
                return x
            x0 = x
        print("Max iterations reached")
        return x

    def _secant_(self, f, x_present, x_previous, tol=1e-6, maxiter=100):
        """
        Finds root of an equation using the secant method.

        Parameters
        ----------
        f : function
            Function to find the root of.
        x_present : float
            Current guess.
        x_previous : float
            Previous guess.
        tol : float, optional
            Tolerance. Default is 1e-6.
        maxiter : int, optional
            Maximum number of iterations. Default is 100.

        Returns
        -------
        root : float
            Root of the equation.
        """
        for _ in range(maxiter):
            x_next = x_present - (f(x_present) * (x_previous - x_present)) / (
                f(x_previous) - f(x_present)
            )
            if np.abs(x_next - x_present) < tol:
                return x_next
            x_previous = x_present
            x_present = x_next
        print("Max iterations reached")
        return x_next

    def get_root(self, f, a, b=None, method="newton", tol=1e-6, maxiter=100):
        """
        Finds the root of an equation.

        Parameters
        ----------
        f : function
            Function to find the root of.
        a : float
            Lower bound of the interval.
        b : float
            Upper bound of the interval.
        methods : str, optional
            Method to use. Available methods are:
            - bisection
            - newton
            - secant

            Default is "newton".
        tol : float, optional
            Tolerance. Default is 1e-6.
        maxiter : int, optional
            Maximum number of iterations. Default is 100.

        Returns
        -------
        root : float
            Root of the equation.
        """
        if b is None and method.lower() != "newton":
            print("b must be specified for bisection and secant methods")
            return None

        method_dicts = {
            "bisection": self._bisection_,
            "newton": self._newton_,
            "secant": self._secant_,
        }
        if method.lower() in method_dicts:
            self.root = method_dicts[method.lower()](f, a, b, tol, maxiter)
            return self.root
        else:
            print(
                f"Invalid method. Available methods are: \n{list(method_dicts.keys())}"
            )
            return None
