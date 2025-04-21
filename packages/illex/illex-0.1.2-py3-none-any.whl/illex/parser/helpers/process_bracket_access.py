import re
import ast
from typing import Any


def process_bracket_access(value: Any, bracket_type: str, inner_content: Any) -> Any:
    """Process bracket access operations ([, (, {)"""
    from illex.core.safe_eval import safe_eval
    try:
        # Evaluate inner content if it's a string
        if isinstance(inner_content, str):
            try:
                # First try to evaluate as a Python literal
                evaluated = ast.literal_eval(inner_content)
            except (ValueError, SyntaxError):
                # If that fails, check if it's a valid identifier
                if re.match(r'^[a-zA-Z_]\w*$', inner_content):
                    evaluated = inner_content  # Treat as a string for dictionary keys
                else:
                    # Use safe_eval for more complex expressions
                    evaluated = safe_eval(inner_content)
        else:
            evaluated = inner_content

        # Apply the access/operation
        if bracket_type == '[':
            return value[evaluated]
        elif bracket_type == '(':
            return value(*evaluated) if isinstance(evaluated, tuple) else value(evaluated)
        elif bracket_type == '{':
            return value(**evaluated) if isinstance(evaluated, dict) else value(evaluated)

    except Exception as e:
        closing_bracket = "]" if bracket_type == "[" else ")" if bracket_type == "(" else "}"
        return f'[Error: {bracket_type}{inner_content}{closing_bracket} -> {str(e)}]'
