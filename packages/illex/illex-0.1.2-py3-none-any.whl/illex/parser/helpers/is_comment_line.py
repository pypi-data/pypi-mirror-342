def is_comment_line(line: str) -> bool:
    """Check if a line is a comment (starts with '\\' or '#')"""
    line = line.strip()
    return line.startswith('\\\\') or line.startswith('#')
