from illex.decorators.function import function
from illex.decorators.multi_param import multi_param_function


@function("replace")
@multi_param_function
def handle_replace(value: str, delimiter: str, substitute: str) -> str:
    try:
        if delimiter.strip() == "":
            delimiter = " "
        parts = value.split(delimiter)
        result = substitute.join(parts)
        return result
    except Exception as e:
        return f"[Replace error: {str(e)}]"
