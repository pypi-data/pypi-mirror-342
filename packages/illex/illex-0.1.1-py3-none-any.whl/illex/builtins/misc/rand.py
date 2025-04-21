from random import randint

from illex.decorators.function import function
from illex.decorators.multi_param import multi_param_function


@function("rand")
@multi_param_function
def handle_rand(start: str, end: str, leading: str = None) -> str:
    try:
        expr = randint(int(start), int(end))
        if leading is None or leading.lower() == "true":
            return f"{expr:02}"
        elif leading.lower() == "false":
            return expr
        else:
            return "[Rand error: leading must be 'true' or 'false'.]"
    except (ValueError, TypeError):
        return "[Rand error: rand expects at least 2 integer values.]"
