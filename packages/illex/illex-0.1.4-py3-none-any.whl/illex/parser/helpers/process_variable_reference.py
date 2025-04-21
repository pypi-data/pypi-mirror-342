from typing import Tuple, Any


def process_variable_reference(text: str, start_idx: int, vars_dict: dict, in_comment: bool) -> Tuple[Any, int]:
    """Process a variable reference starting with @ and return the value and new index"""
    from illex.parser.helpers import extract_bracket_content, process_bracket_access
    from illex.parser.steps import replace_variables
    n = len(text)
    i = start_idx + 1  # Skip the @
    var_name = []

    # Extract variable name
    while i < n and (text[i].isalnum() or text[i] == '_'):
        var_name.append(text[i])
        i += 1
    var_name = ''.join(var_name)

    # Check for backslash escape character
    escaped = False
    if i < n and text[i] == '\\':
        escaped = True
        i += 1  # Skip the backslash

    # Process indices/accesses [ ] ( ) { }
    indices = []
    if not escaped and not in_comment:  # Only process indices if not escaped and not in comment
        while i < n and text[i] in ['[', '(', '{']:
            bracket_type = text[i]
            inner_content, _, new_i = extract_bracket_content(text, i)
            i = new_i

            # Process variables recursively in the inner content
            processed_inner = replace_variables(inner_content, vars_dict)

            # Store the processed content and bracket type
            indices.append({
                'type': bracket_type,
                'content': processed_inner
            })

    # Resolve the base value
    value = vars_dict.get(var_name, f'@{var_name}')

    # Apply indices/accesses
    for index_info in indices:
        value = process_bracket_access(
            value, index_info['type'], index_info['content'])
        if isinstance(value, str) and value.startswith('[Error:'):
            break

    return value, i
