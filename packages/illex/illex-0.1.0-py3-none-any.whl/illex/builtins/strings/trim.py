from illex.decorators.function import function


@function("trim")
def trim(expr: str) -> str: return expr.strip()
