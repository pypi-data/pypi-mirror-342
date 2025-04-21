def process_assignments(text: str, variables: dict) -> str:
    """Phase 1: Process assignments with real-time substitution"""
    from illex.parser.helpers import is_comment_line, process_variable_assignment
    output = []
    i = 0
    n = len(text)

    while i < n:
        current_line_start = text.rfind('\n', 0, i) + 1
        current_line = text[current_line_start:].split('\n')[0]
        in_comment = is_comment_line(current_line)

        if text[i] == '@' and not in_comment:
            result_text, i = process_variable_assignment(text, i, variables)
            output.append(result_text)
        else:
            output.append(text[i])
            i += 1

    return ''.join(output)
