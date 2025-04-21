import re
from typing import Any


def process_handlers(text: str, variables: dict) -> Any:
    """Phase 3: Process handlers with regex - modified to preserve types"""
    from illex.core.registry import registry
    from illex.parser.helpers import process_handler_call
    
    result = text

    # If the result is already a Python object, return it directly
    if not isinstance(result, str):
        return result

    handler_pattern = re.compile(r':(\w+)\(((?:[^()]*|\([^()]*\))*)\)')

    # If we have just one handler with nothing before or after, preserve its type
    match = handler_pattern.match(result.strip())
    if match and match.end() == len(result.strip()):
        tag, expr_part = match.groups()
        return process_handler_call(tag, expr_part, variables)

    # Normal processing for more complex cases
    last_result = None
    while result != last_result:
        last_result = result
        match = handler_pattern.search(result)
        if not match:
            break

        tag, expr_part = match.groups()
        if tag in registry:
            # Process variables in the expression part before calling the handler
            resolved = process_handler_call(tag, expr_part, variables)

            # If the result is a non-string object, store it in a temporary variable
            if not isinstance(resolved, str) and not isinstance(resolved, (int, float, bool, type(None))):
                temp_var_name = f"__temp_{tag}_{len(variables)}"
                variables[temp_var_name] = resolved
                result = result.replace(match[0], f"@{temp_var_name}", 1)
            else:
                result = result.replace(match[0], str(resolved), 1)
        else:
            result = result.replace(match[0], f"[Unsupported: {tag}]", 1)

    return result
