from math import ceil

from illex.decorators.function import function
from illex.decorators.math import math_function


@function("ceil")
@math_function
def handle_ceil(result): return ceil(float(result))
