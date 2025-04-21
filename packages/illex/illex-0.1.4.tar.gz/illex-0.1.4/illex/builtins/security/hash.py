from hashlib import md5, sha1, sha256, sha512

from illex.decorators.function import function
from illex.decorators.multi_param import multi_param_function


@function("hash")
@multi_param_function
def handle_hash(text: str, hash_type: str = "md5"):
    return {
        "md5": md5(text.encode()).hexdigest(),
        "sha1": sha1(text.encode()).hexdigest(),
        "sha256": sha256(text.encode()).hexdigest(),
        "sha512": sha512(text.encode()).hexdigest(),
    }.get(hash_type, md5(text.encode()).hexdigest())
