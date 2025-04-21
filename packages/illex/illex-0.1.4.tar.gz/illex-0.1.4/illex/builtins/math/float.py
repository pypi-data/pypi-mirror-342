from illex.decorators.function import function
from illex.decorators.math import math_function


@function("float")
@math_function
def handle_float(result): return float(result)
