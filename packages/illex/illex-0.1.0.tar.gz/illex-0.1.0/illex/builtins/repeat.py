from illex.decorators.function import function
from illex.decorators.multi_param import multi_param_function


@function("repeat")
@multi_param_function
def handle_repeat(expr: any, times: int = 1):
    try:
        times = int(times)
        if times < 0 or times > 1000:
            return "Error: 'times' must be between 0 and 1000"
        return '\n'.join(str(expr) for _ in range(times))
    except ValueError:
        return "Error: 'times' must be an integer"
