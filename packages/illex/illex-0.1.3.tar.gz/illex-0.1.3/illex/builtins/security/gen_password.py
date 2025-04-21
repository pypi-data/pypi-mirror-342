from random import choices
from string import (
    ascii_lowercase,
    ascii_uppercase,
    punctuation,
    digits
)
from illex.decorators.function import function
from illex.decorators.multi_param import multi_param_function


@function("gen_password")
@function("genPassword")
@function("genpassword")
@multi_param_function
def handle_gen_password(
    lenght: str,
    lower: str = None,
    upper: str = None,
    with_digits: str = None,
    with_punctuation: str = None
):
    chars = ""
    
    if lower is None or lower.lower() == "true":
        chars += ascii_lowercase

    if upper is None or upper.lower() == "true":
        chars += ascii_uppercase

    if with_digits is None or with_digits.lower() == "true":
        chars += digits

    if with_punctuation is None or with_punctuation.lower() == "true":
        chars += punctuation

    if not chars:
        chars = ascii_lowercase

    return ''.join(choices(chars, k=int(lenght)))
