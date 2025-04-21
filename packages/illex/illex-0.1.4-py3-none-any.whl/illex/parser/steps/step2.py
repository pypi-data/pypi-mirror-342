from typing import Any


def replace_variables(text: str, vars_dict: dict) -> Any:
    """Replace variables in text with their values from vars_dict"""
    from illex.parser.helpers import is_comment_line, process_variable_reference
    if not isinstance(text, str):
        return text

    output = []
    i = 0
    n = len(text)

    while i < n:
        # Check if we're in a comment line
        current_line_start = text.rfind('\n', 0, i) + 1
        current_line = text[current_line_start:].split('\n')[0]
        in_comment = is_comment_line(current_line)

        if text[i] == '@' and not in_comment:
            value, i = process_variable_reference(
                text, i, vars_dict, in_comment)
            output.append(value)
        else:
            output.append(text[i])
            i += 1

    # If there's only one element and it's not text, return it directly
    if len(output) == 1 and not isinstance(output[0], str):
        return output[0]

    # Otherwise, join everything as text
    return ''.join(str(item) for item in output)
