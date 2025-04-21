import ipaddress
from illex.decorators.function import function


@function("is_public")
@function("isPublic")
@function("ispublic")
def is_public(expr: str) -> str:
    try:
        return ipaddress.ip_address(expr).is_private
    except (ValueError, Exception) as e:
        return f"[CIDR error: {e}]"
