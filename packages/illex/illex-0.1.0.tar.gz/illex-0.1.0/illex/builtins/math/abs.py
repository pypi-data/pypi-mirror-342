from illex.decorators.function import function
from illex.decorators.math import math_function


@function("abs")
@math_function
def handle_abs(result): return abs(int(result))
