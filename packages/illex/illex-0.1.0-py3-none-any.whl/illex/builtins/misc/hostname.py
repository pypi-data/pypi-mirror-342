import re

from illex.decorators.function import function
from illex.decorators.multi_param import multi_param_function


@function("hostname")
@multi_param_function
def hostname(value: str, divider: str = "-", is_upper: str = None) -> str:
    try:
        res = re.sub(r"\W+|\s+", divider, value)
        if is_upper is None or is_upper.lower() == "true":
            return res.upper()
        elif is_upper.lower().strip() == "false":
            return res
        else:
            return "[Hostname error: is_upper must be 'true' or 'false'.]"
    except (ValueError, TypeError, Exception) as e:
        return f"[Hostname error: hostname expects only 2 values: {e}]"
