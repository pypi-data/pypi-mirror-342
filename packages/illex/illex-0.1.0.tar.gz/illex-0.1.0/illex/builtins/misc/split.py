from illex.decorators.function import function
from illex.decorators.multi_param import multi_param_function


@function("split")
@multi_param_function
def handle_split(string: str, delimiter: str) -> str:
    try:
        parts = string.split(delimiter)
        return parts
    except Exception as e:
        return f"[Split error: {str(e)}]"
