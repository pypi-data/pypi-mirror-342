from illex.decorators.function import function
from illex.decorators.math import math_function


@function("int")
@math_function
def handle_int(result): return int(result)
