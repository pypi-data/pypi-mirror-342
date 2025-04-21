from functools import wraps


def network_function(func):
    """Decorator for IP-related handlers"""
    @wraps(func)
    def wrapper(expr: str):
        try:
            return func(*expr.split(','))
        except ValueError as e:
            return f"[Error: {e}]"
    return wrapper
