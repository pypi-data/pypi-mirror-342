from math import fabs

from illex.decorators.function import function
from illex.decorators.math import math_function


@function("fabs")
@math_function
def handle_fabs(result): return fabs(float(result))