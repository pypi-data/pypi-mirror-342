from typing import Any, Dict

from illex.parser.steps import (
    substitute_placeholders,
    process_assignments,
    replace_variables,
    process_handlers
)


def parse(text: str, params: dict = {}) -> Any:
    """Main expression parser using state machine"""
    from illex import variables

    # Phase 0: Substitute placeholders with regex
    text = substitute_placeholders(text, params)

    # Phase 1: Process assignments with real-time substitution
    text = process_assignments(text, variables)

    # Phase 2: Replace remaining variables
    result = replace_variables(text, variables)

    # Phase 3: Process handlers with regex
    result = process_handlers(result, variables)

    # Replace variables again to capture any temporary ones created
    if isinstance(result, str):
        final_result = replace_variables(result, variables)
        return final_result
    else:
        return result