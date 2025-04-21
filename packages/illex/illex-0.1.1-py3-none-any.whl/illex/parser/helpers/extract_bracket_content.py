from typing import Tuple


def extract_bracket_content(text: str, start_idx: int) -> Tuple[str, int, int]:
    """Extract content inside brackets and return the content, start and end indices"""
    bracket_type = text[start_idx]
    bracket_depth = 1
    i = start_idx + 1
    n = len(text)
    index_start = i

    while i < n and bracket_depth > 0:
        if text[i] == bracket_type:
            bracket_depth += 1
        elif text[i] in [']', ')', '}']:
            bracket_depth -= 1
        i += 1

    # Extract inner content
    inner_content = text[index_start:i-1]
    return inner_content, index_start, i
