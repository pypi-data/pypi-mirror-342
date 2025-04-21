from typing import Tuple


def extract_value_until_delimiter(text: str, start_idx: int) -> Tuple[str, int]:
    """Extract a value until a delimiter is encountered"""
    i = start_idx
    n = len(text)
    value = []
    bracket_depth = 0
    in_string = False
    string_char = None

    while i < n:
        current_char = text[i]

        if not in_string:
            if current_char in '([{':
                bracket_depth += 1
            elif current_char in ')]}':
                bracket_depth -= 1
            elif current_char in ('"', "'", "`"):
                in_string = True
                string_char = current_char
            elif current_char == '@' and bracket_depth == 0:
                break
            elif current_char == '\n' and bracket_depth == 0:
                break

        if current_char == '\\':
            value.append(current_char)
            i += 1
            if i < n:
                value.append(text[i])
            i += 1
            continue

        value.append(current_char)
        i += 1

        if in_string and current_char == string_char:
            in_string = False

    value_str = ''.join(value).strip()
    return value_str, i
