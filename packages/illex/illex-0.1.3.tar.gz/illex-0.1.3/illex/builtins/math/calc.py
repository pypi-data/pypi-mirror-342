from illex.decorators.function import function
from illex.decorators.math import math_function


@function("calc")
@math_function
def handle_calc(result): return int(result)
