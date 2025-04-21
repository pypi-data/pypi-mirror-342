from illex.decorators.function import function
from illex.decorators.multi_param import multi_param_function


@function("list")
@multi_param_function
def handle_list(*args):
    return list(args)
