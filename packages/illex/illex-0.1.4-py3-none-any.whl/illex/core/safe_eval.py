import ast
from illex.core.safe_globals import SAFE_GLOBALS

BLOCKED_WORDS = {"__class__", "__bases__", "__subclasses__", "__globals__"}

ALLOWED_NODES = {
    ast.Expression, ast.Constant, ast.List, ast.Tuple, ast.Set, ast.Dict,
    ast.BinOp, ast.UnaryOp, ast.Compare, ast.Name, ast.Call, ast.Load
}

ALLOWED_BINOPS = {ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow}
ALLOWED_UNARYOPS = {ast.UAdd, ast.USub, ast.Not}
ALLOWED_CMPOPS = {ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.In, ast.NotIn}


class NameToStr(ast.NodeTransformer):
    def visit_Name(self, node):
        return ast.Constant(value=node.id)


def is_safe(node):
    if type(node) not in ALLOWED_NODES:
        return False
    match node:
        case ast.Expression(body=body): return is_safe(body)
        case ast.Constant(): return True
        case ast.BinOp(left=left, op=op, right=right):
            return type(op) in ALLOWED_BINOPS and is_safe(left) and is_safe(right)
        case ast.UnaryOp(op=op, operand=operand):
            return type(op) in ALLOWED_UNARYOPS and is_safe(operand)
        case ast.Compare(left=left, ops=ops, comparators=comparators):
            return all(type(op) in ALLOWED_CMPOPS for op in ops) and is_safe(left) and all(is_safe(c) for c in comparators)
        case ast.Name(id=name): return name in SAFE_GLOBALS
        case ast.Call(func=func, args=args):
            return isinstance(func, ast.Name) and func.id in SAFE_GLOBALS and all(is_safe(arg) for arg in args)
        case ast.List(elts=elts) | ast.Tuple(elts=elts) | ast.Set(elts=elts):
            return all(is_safe(el) for el in elts)
        case ast.Dict(keys=keys, values=values):
            return all(is_safe(k) and is_safe(v) for k, v in zip(keys, values))
        case _: return False

def safe_eval(expr: str):
    if any(word in expr for word in BLOCKED_WORDS):
        return "Não é possível acessar esse recurso."

    try:
        tree = ast.parse(expr, mode='eval')
        tree = NameToStr().visit(tree)
        ast.fix_missing_locations(tree)

        if not is_safe(tree):
            return "Operação não permitida."

        return eval(compile(tree, "<safe_eval>", "eval"), {"__builtins__": None}, SAFE_GLOBALS)
    except Exception:
        return expr
