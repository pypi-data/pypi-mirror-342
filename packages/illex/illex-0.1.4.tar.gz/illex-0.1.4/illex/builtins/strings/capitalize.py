from illex.decorators.function import function


@function("capitalize")
def capitalize(expr: str) -> str: return expr.capitalize()
