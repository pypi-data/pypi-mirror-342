# ILLEX: Inline Language for Logic and EXpressions

## Overview
ILLEX is a lightweight scripting language for structured text processing, featuring variable substitution, inline expressions, and customizable handlers. Built on a state machine-based parser with safe evaluation and extensibility.

## Key Features
- Secure expression parsing with controlled variable evaluation
- Inline variable assignments and references (e.g., `@var = value`)
- Customizable function handlers for advanced text transformation
- Recursive resolution of expressions with safe execution
- Loops, conditionals, logical and mathematical operators

## Installation
```bash
pip install illex
```

## Basic Usage

### Variable Substitution
```python
import illex
illex.parse("Hello, {name}!", {"name": "World"})
# Result: 'Hello, World!'
```

### Variable Assignment and Reference
```python
text = """
@name = John
@age = 30
Name: @name, Age: @age
"""
illex.parse(text, {})
# Result: 'Name: John, Age: 30'
```

### Mathematical Expressions
```python
text = """
@x = 10
@y = 20
Sum: @x + @y
Product: :calc(@x * @y)
"""
illex.parse(text, {})
# Result: 'Sum: 10 + 20\nProduct: 200'
```

## Syntax Structure

### Variables
- Assignment: `@variable = value`
- Reference: `@variable`
- List/Dictionary access: `@list[0]`, `@dict["key"]`, `@dict[key]`

### Built-in Functions
Functions are called with the `:` prefix followed by the function name and arguments in parentheses.

Example: `:function(arg1, arg2)`

## Built-in Functions

### String Manipulation
- `:uppercase(text)` - Converts text to uppercase
- `:lowercase(text)` - Converts text to lowercase
- `:capitalize(text)` - Capitalizes the first letter of text
- `:trim(text)` - Removes whitespace from both ends
- `:replace(text, search, replace)` - Replaces occurrences

### Math Functions
- `:calc(expression)` - Evaluates a mathematical expression
- `:int(value)` - Converts to integer
- `:float(value)` - Converts to floating point
- `:abs(value)` - Absolute value (integer)
- `:fabs(value)` - Absolute value (float)
- `:floor(value)` - Rounds down
- `:ceil(value)` - Rounds up

### Date Functions
- `:date(format)` - Returns formatted date
  - Special formats: `today`, `now`, `yesterday`, `tomorrow`
  - Supports standard date format strings (e.g., `%d/%m/%Y`)

### Lists and Dictionaries
- `:list(item1, item2, ...)` - Creates a list
- `:split(text, delimiter)` - Splits text into a list
- `:options(key1=value1, key2=value2, ...)` - Creates a dictionary

### Conditional Functions
- `:if(condition, true_result, false_result)` - Conditional expression

### Network Functions
- `:cidr(mask)` - Converts to CIDR notation
- `:is_public(ip)` - Checks if IP is public
- `:resolve(host)` - Resolves hostname to IP

### Security Functions
- `:hash(text, type)` - Generates hash (md5, sha1, sha256, sha512)
- `:encrypt(text, key, type)` - Encrypts text
- `:decrypt(text, key, type)` - Decrypts text
- `:gen_password(length, lower, upper, with_digits, with_punctuation)` - Generates password

### Utilities
- `:repeat(text, times)` - Repeats text N times
- `:hostname(value, separator, is_upper)` - Formats as hostname
- `:rand(start, end, leading)` - Generates random number

## Command Line Usage

```bash
# Process .illex file
illex run file.illex

# Process with variables (key=value format)
illex run file.illex --vars name=John age=30

# Process with variables from JSON/YAML file
illex run file.illex --vars config.json

# Save result to file
illex run file.illex -o  # Saves to file.illex.out
```

## Extensibility

### Creating New Handlers

```python
from illex.decorators.handler import handler

@handler("my_function")
def my_function(text):
    return text.upper()
```

### Creating Math Functions

```python
from illex.decorators.handler import handler
from illex.decorators.math import math_function

@handler("square")
@math_function
def square(value):
    return value ** 2
```

## Advanced Examples

### Text Processing with Variables

```
@name = "Jane Smith"
@email = "jane@example.com"
@age = 28

User Profile:
Name: @name
Email: @email
Age: @age
Adult: :if(@age >= 18, "Yes", "No")
```

### List Operations

```
@fruits = :list("apple", "banana", "orange")
@favorite_fruit = @fruits[1]

Available fruits:
@fruits[0]
@fruits[1]
@fruits[2]

My favorite fruit is @favorite_fruit.
```

### Dynamic Content Generation

```
@server = "prod"
@environment = :if(@server == "prod", "Production", "Development")
@current_date = :date(today)

Environment Report - @current_date

Environment: @environment
Server: :uppercase(@server)
Status: :if(@environment == "Production", "CRITICAL", "Normal")
```

### Network Processing

```
@domain = "example.com"
@ip = :resolve(@domain)
@hostname = :hostname(@domain)

Network Information:
Domain: @domain
IP: @ip
Hostname: @hostname
Public IP: :if(:is_public(@ip), "Yes", "No")
```

## Security

ILLEX implements secure expression evaluation:

- Uses `safe_eval` to prevent malicious code execution
- Blocked words list (`__class__`, `__bases__`, `__subclasses__`, `__globals__`)
- Explicitly controlled allowed AST nodes
- Controlled allowed binary, unary, and comparison operators
- Safe globals limited to basic functions like `list`, `dict`, `str`, etc.

## Internal Implementation

ILLEX execution follows four main phases:

1. **Phase 0**: Placeholder substitution `{var}` with parameter values
2. **Phase 1**: Variable assignment processing `@var = value` 
3. **Phase 2**: Variable reference substitution `@var`
4. **Phase 3**: Handler call processing `:func(args)`

This design allows for nested and recursive expression processing.

## Best Practices

- Use comments with `\\` or `#` to document your code
- Prefer specific handlers (`:calc`, `:int`) for operations rather than complex expressions
- Avoid excessive function nesting
- Use variables to store intermediate results
- Escape commas in function arguments with `\,` when necessary

## Limitations
- No support for custom function definitions in ILLEX code itself
- Expression evaluation is limited for security
- No full flow control (only simple conditional structures)

## License

ILLEX is licensed under GNU General Public License v3.0 (GPL-3.0).

Copyright (C) 2023-2025 Gustavo Zeloni

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

Full license text: https://github.com/gzeloni/illex/blob/main/LICENSE
