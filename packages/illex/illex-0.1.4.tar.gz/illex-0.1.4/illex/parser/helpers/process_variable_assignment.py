import re
from typing import Tuple


def process_variable_assignment(text: str, start_idx: int, variables: dict) -> Tuple[str, int]:
    """Process a variable assignment starting at the given index"""
    from illex.parser.helpers import extract_value_until_delimiter, process_handler_call, evalv
    i = start_idx
    n = len(text)

    var_start = i
    i += 1  # Skip the @

    # Extract variable name
    var_name = []
    while i < n and (text[i].isalnum() or text[i] == '_'):
        var_name.append(text[i])
        i += 1
    var_name = ''.join(var_name)

    # Skip whitespace
    while i < n and text[i].isspace():
        i += 1

    # Check if this is an assignment
    if i < n and text[i] == '=' and (i+1 >= n or text[i+1] != '='):
        i += 1  # Skip the =

        # Skip whitespace
        while i < n and text[i].isspace():
            i += 1

        # Extract the value
        value_str, i = extract_value_until_delimiter(text, i)

        # Check if the value is a handler call
        handler_match = re.match(
            r'^:(\w+)\(((?:[^()]*|\([^()]*\))*)\)$', value_str)
        if handler_match:
            tag, expr_part = handler_match.groups()
            variables[var_name] = process_handler_call(
                tag, expr_part, variables)
        else:
            variables[var_name] = evalv(value_str, variables)

        # Skip whitespace
        while i < n and text[i].isspace():
            i += 1

        return '', i
    else:
        # Not an assignment, return the original text
        return text[var_start:i], i
