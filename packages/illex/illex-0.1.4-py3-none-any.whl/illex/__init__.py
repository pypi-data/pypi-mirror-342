"""
ILLEX – Inline Language for Logic and EXpressions
A lightweight scripting language for structured text processing,  
featuring variable substitution, inline expressions, and customizable handlers.  
Built on a state machine-based parser with safe evaluation and extensibility.

Features:
    - Secure expression parsing with controlled variable evaluation
    - Inline variable assignments and references (e.g., `@var = value`)
    - Customizable function handlers for advanced text transformation
    - Recursive resolution of expressions with safe execution
    - Loops, conditionals, logical and mathematical operators

Extensibility:
    - New handlers can be added dynamically using decorators:
        >>> from illex.decorators.handler import handler
        >>> @handler("foo")
        ... def bar(): return baz
        OR
        >>> from illex.decorators.handler import handler
        >>> from illex.decorators.math import math_function
        >>> @handler("foo")
        >>> @math_function
        ... def bar(): return baz

    - Existing handlers can be modified or replaced:
        >>> from illex.registry import registry
        >>> registry["math"] = new_math_function  # Override default math handler

Modules:
    - handlers: Built-in transformation functions
    - decorators: Utilities for extending illex
    - registry: Global registry of handlers
    - parser: Core engine implementing illex logic

Usage:
    >>> import illex
    >>> illex.parse("Hello, {name}!", {"name": "Gustavo"})
    'Hello, Gustavo!'

    >>> illex.parse("@x = 10\nResult: @x * 2", {})
    'Result: 20'

Version: 0.1.2  
Author: Gustavo Zeloni  
"""


from illex.parser.parse import parse
from illex.core.variables import variables
from illex import builtins, decorators, parser
from illex.decorators.function import load_functions


load_functions('illex.builtins')


__version__ = "1.0.0"
__all__ = [
    "builtins",
    "decorators",
    "parser",
    "parse",
    "variables",
    "__version__"
]
