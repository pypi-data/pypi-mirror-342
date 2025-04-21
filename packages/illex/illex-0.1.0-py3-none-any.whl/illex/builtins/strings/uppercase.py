from illex.decorators.function import function


@function("uppercase")
def uppercase(expr: str) -> str: return expr.upper()
