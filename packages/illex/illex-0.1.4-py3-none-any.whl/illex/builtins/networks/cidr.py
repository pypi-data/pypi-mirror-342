import ipaddress
from illex.decorators.function import function


@function("cidr")
def cidr(expr: str) -> str:
    try:
        return f"/{ipaddress.IPv4Network(f'0.0.0.0/{expr}').prefixlen}"
    except ipaddress.NetmaskValueError as e:
        return f"[CIDR error: {e}.]"
    except ipaddress.AddressValueError as e:
        return f"[CIDR error: {e}.]"
    except Exception:
        return "[CIDR error: Unknown error.]"
