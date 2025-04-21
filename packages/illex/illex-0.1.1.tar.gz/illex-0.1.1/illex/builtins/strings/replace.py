from illex.decorators.function import function
from illex.decorators.multi_param import multi_param_function


@function("replace")
@multi_param_function
def replace(value: str, delimiter: str, substitute: str) -> str:
    try:
        return value.replace(delimiter, substitute)
    except (ValueError, TypeError, Exception):
        return f"[Replace error: replace expects 3 values.]"
