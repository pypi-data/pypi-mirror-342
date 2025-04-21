from functools import wraps


def multi_param_function(func):
    """Decorator for multi parameter handlers"""
    @wraps(func)
    def wrapper(expr: str):
        try:
            args = []
            current_arg = []
            depth = 0
            in_quotes = False
            quote_char = None
            escape_next = False

            i = 0
            while i < len(expr):
                char = expr[i]

                if char == '\\' and i + 1 < len(expr) and expr[i + 1] == ',':
                    current_arg.append(',')
                    i += 2
                    continue

                if char in '"\'':
                    if not in_quotes:
                        in_quotes = True
                        quote_char = char
                    elif char == quote_char:
                        in_quotes = False
                        quote_char = None
                    else:
                        current_arg.append(char)

                elif char in '([{':
                    depth += 1
                    current_arg.append(char)
                elif char in ')]}':
                    depth -= 1
                    current_arg.append(char)

                elif char == "," and depth == 0 and not in_quotes:
                    args.append(''.join(current_arg).strip())
                    current_arg = []
                else:
                    current_arg.append(char)

                i += 1

            if current_arg:
                args.append(''.join(current_arg).strip())

            processed_args = []
            for arg in args:
                arg = arg.strip()
                if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
                    if len(arg) >= 2:
                        arg = arg[1:-1]
                processed_args.append(arg)

            for i, arg in enumerate(processed_args):
                if '\\,' in arg:
                    processed_args[i] = arg.replace('\\,', ',')

            return func(*processed_args)
        except ValueError as e:
            return f"[Error: {e}]"

    return wrapper
