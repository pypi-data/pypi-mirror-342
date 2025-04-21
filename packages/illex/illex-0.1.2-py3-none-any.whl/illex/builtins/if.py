from illex.core.safe_eval import safe_eval
from illex.decorators.function import function
from illex.decorators.multi_param import multi_param_function


@function("if")
@multi_param_function
def handle_if(condition: any, true_result: str, false_result: str):
    return true_result if safe_eval(condition) else false_result
