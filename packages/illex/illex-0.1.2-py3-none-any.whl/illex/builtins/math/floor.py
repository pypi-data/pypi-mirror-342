from math import floor

from illex.decorators.function import function
from illex.decorators.math import math_function


@function("floor")
@math_function
def handle_floor(result): return floor(float(result))
