from functools import wraps
from sympy import SympifyError, sympify
from illex import parse


def math_function(func):
    """Decorator for math operations"""
    @wraps(func)
    def wrapper(expr: str):
        try:
            expr = parse(expr)
            return func(sympify(expr).evalf())
        except (SympifyError, Exception) as e:
            return f"[{func.__name__.title()} error: {e}]"
    return wrapper
