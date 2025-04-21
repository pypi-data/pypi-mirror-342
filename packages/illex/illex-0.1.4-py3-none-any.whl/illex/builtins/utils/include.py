import illex
from illex.decorators.function import function
from illex.decorators.multi_param import multi_param_function


@function("include")
@multi_param_function
def handle_include(*paths):
    import inspect
    in_assignment = any(
        'process_variable_assignment' in f.function for f in inspect.stack())

    all_vars = {}
    output = []

    for p in paths:
        if not p.endswith('.illex'):
            p += '.illex'

        try:
            with open(p, 'r') as f:
                content = f.read()

            vars_dict = {}
            from illex.parser.steps import process_assignments
            process_assignments(content, vars_dict)
            all_vars.update(vars_dict)

            if not in_assignment:
                result = illex.parse(content, {})
                if result:
                    output.append(str(result))

        except FileNotFoundError:
            output.append(f"[Include error: File '{p}' not found]")
        except Exception as e:
            output.append(f"[Include error: {str(e)}]")

    return all_vars if in_assignment else '\n'.join(output)
