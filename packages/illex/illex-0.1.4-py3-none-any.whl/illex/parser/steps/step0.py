import re


def substitute_placeholders(text: str, params: dict) -> str:
    """Phase 0: Substitute placeholders with regex"""
    return re.sub(r'\{(\w+)\}', lambda m: str(params.get(m[1], m[0])), text.strip())
