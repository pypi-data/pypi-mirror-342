import socket
from illex.decorators.function import function


@function("resolve")
def resolve(expr: str) -> str:
    try:
        return socket.gethostbyname(expr)
    except (socket.gaierror, Exception):
        return "[Resolve error: Name or service not known.]"
