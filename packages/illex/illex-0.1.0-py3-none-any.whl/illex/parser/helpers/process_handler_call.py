from typing import Any

from illex.core.registry import registry


def process_handler_call(tag: str, expr_part: str, variables: dict) -> Any:
    """Process a handler call with given tag and expression"""
    from illex.parser.steps import replace_variables

    if tag not in registry:
        return f"[Unsupported: {tag}]"

    # Only process expression if it exists
    expr = replace_variables(expr_part, variables) if expr_part else None

    # Call handler with or without expression based on what's provided
    return registry[tag](expr) if expr is not None else registry[tag]()
