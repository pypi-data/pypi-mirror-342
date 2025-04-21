from illex.decorators.function import function


@function("lowercase")
def lowercase(expr: str) -> str: return expr.lower()
