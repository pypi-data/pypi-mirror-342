# ILLEX: Inline Language for Logic and EXpressions
A lightweight scripting language for structured text processing with variable substitution, inline expressions, and extensible handlers.

## Documentation

For full documentation and advanced usage examples, see the [ILLEX Documentation](https://docs.illex.dev).

## Features

- Secure expression parsing with controlled variable evaluation
- Variable assignments and references (`@var = value`)
- Mathematical expressions and conditional logic
- Customizable function handlers for text transformation
- Built-in functions for string, math, date, network, and security operations

## Installation

```bash
pip install illex
```

## Usage

```python
import illex

# Variable substitution
illex.parse("Hello, {name}!", {"name": "World"})
# Result: 'Hello, World!'

# Assignment and reference
text = """
@name = John
@age = 30
Name: @name, Age: @age
"""
illex.parse(text, {})
# Result: 'Name: John, Age: 30'

# Mathematical expressions
illex.parse("Sum: :calc(10 + 20)", {})
# Result: 'Sum: 30'
```

## CLI Usage

```bash
# Process file
illex run file.illex

# With variables
illex run file.illex --vars name=John age=30

# Load variables from file
illex run file.illex --vars config.json
```

## Extending ILLEX

```python
from illex.decorators.function import function

@function("my_function")
def my_function(text):
    return text.upper()
```

## License

ILLEX is licensed under GNU General Public License v3.0 (GPL-3.0).

Copyright (C) 2023-2025 Gustavo Zeloni

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

Full license text: https://github.com/gzeloni/illex/blob/main/LICENSE