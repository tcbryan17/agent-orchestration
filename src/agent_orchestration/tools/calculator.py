"""Safe arithmetic over Decimal.

WHY not eval(): the expression comes from a model that read untrusted filing text. We parse
it with `ast` and allow only numbers, + - * /, unary minus and parentheses. Decimal avoids
float rounding in money maths.
"""

import ast
import operator
from collections.abc import Callable
from decimal import Decimal, InvalidOperation

_BINARY: dict[type[ast.operator], Callable[[Decimal, Decimal], Decimal]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def calculate(expression: str) -> Decimal:
    """Evaluate `expression`; raise ValueError for anything outside plain arithmetic."""
    try:
        tree = ast.parse(expression.strip(), mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"not a valid arithmetic expression: {expression!r}") from exc
    return _eval(tree.body)


def _eval(node: ast.expr) -> Decimal:
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
        if isinstance(node.value, bool):
            raise ValueError("booleans are not allowed")
        return Decimal(str(node.value))
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
        left, right = _eval(node.left), _eval(node.right)
        try:
            return _BINARY[type(node.op)](left, right)
        except (ZeroDivisionError, InvalidOperation) as exc:
            raise ValueError("division by zero or invalid operation") from exc
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval(node.operand)
    raise ValueError(f"disallowed expression element: {type(node).__name__}")
