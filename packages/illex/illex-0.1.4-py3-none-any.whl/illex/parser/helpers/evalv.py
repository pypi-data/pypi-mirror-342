import ast
from typing import Any


def evalv(value_str: str, variables: dict) -> Any:
    """Evaluate a value string to a Python object if possible"""
    from illex.parser.steps import replace_variables
    
    # Process variables in the value
    substituted_value = replace_variables(value_str, variables)

    # If the result is not a string, use it directly
    if not isinstance(substituted_value, str):
        return substituted_value

    try:
        # Try to convert to a Python literal using ast.literal_eval
        return ast.literal_eval(substituted_value)
    except (ValueError, SyntaxError, TypeError):
        # If that fails, keep it as a string
        return substituted_value
    except Exception as e:
        # Log other unexpected errors
        return f'[Error: {str(e)}]'
