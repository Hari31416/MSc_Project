from calculus import Derivative, Integration
import random
from ode import ODE
import math


def f(x):
    return x ** 3 + x ** 2 + x + 1


def g(x):
    return math.sin(x)


def h(x, y):
    return x + y


methods = ["fd", "bd", "cd"]
orders = ["first", "second"]
errors = ["first", "second", "fourth"]

# For Derivative
def main():
    method = random.choice(methods)
    order = random.choice(orders)
    error = random.choice(errors)
    num = random.randint(1, 10)
    d = Derivative()
    try:
        value = d.derivative(f, num, order, method, error)
        print(f"{value} {method} {order} {error}")
    except Exception as e:
        print(f"{method} {order} {error}")
        raise e


# For Integration
def main2():
    methods = [
        "as_sum",
        "multi_trapzoid",
        "simpson13",
        "simpson13multi",
        "simpson38",
        "simpson38multi",
    ]
    a = random.randint(1, 10)
    b = random.randint(a, 10)
    n = random.randint(50, 1000)
    method = random.choice(methods)
    i = Integration()
    try:
        value = i.integrate(f, a, b, method, n)
        print(f"{value} {method} {a} {b} {n}")
    except Exception as e:
        print(f"{method} {a} {b} {n}")
        # print(e)
        raise e


# For ODE
def main3():
    methods = [
        "euler",
        "euler_modified",
        "heun",
        "ralston",
        "midpoint",
        "rk3",
        "rk4",
        "rk5",
    ]
    method = random.choice(methods)
    # a = random.randint(1, 10)
    # b = random.randint(a, 10)
    # n = random.randint(50, 200)
    # x = random.randint(1, 10)
    a = 0
    b = 4
    n = 30
    x = 5
    ode = ODE()
    try:
        value = ode.solve(h, a, b, x, n, method)
        print(f"{value} {method} {a} {b} {n}")
    except Exception as e:
        print(f"{method} {a} {b} {n}")
        raise e


if __name__ == "__main__":
    for i in range(100):
        # main()
        # main2()
        main3()
