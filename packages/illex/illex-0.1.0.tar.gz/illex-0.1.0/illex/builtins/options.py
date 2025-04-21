from illex.decorators.function import function
from illex.decorators.multi_param import multi_param_function


@function("options")
@multi_param_function
def handle_options(*args):
    result = {}
    for arg in args:
        if "=" not in arg:
            raise ValueError(f"Formato inválido: {arg}")
        key, value = arg.split("=", 1)
        result[key.strip()] = value.strip()
    return result