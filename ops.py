from dataclasses import dataclass
from operator import add, sub, mul, truediv
from typing import Callable, Optional, Tuple

from PySimpleGUI import WIN_CLOSED


def toggle_sign(x: float) -> float:
    return -x


def swap(x: float, y: float) -> Tuple[float, float]:
    return y, x


#@dataclass(slots=True)
@dataclass
class Operator:
    opcode: str
    arity_in: int
    arity_out: int
    func: Optional[Callable]
    doc: Optional[str]


operators = {
    '+': Operator(opcode='+', arity_in=2, arity_out=1, func=add, doc='Addition'),
    '-': Operator(opcode='-', arity_in=2, arity_out=1, func=sub, doc='Subtraction'),
    '*': Operator(opcode='*', arity_in=2, arity_out=1, func=mul, doc='Multiplication'),
    '/': Operator(opcode='/', arity_in=2, arity_out=1, func=truediv, doc='Division'),
    '^': Operator(opcode='^', arity_in=2, arity_out=1, func=pow, doc='Power'),
    '+/-': Operator(opcode='+/-', arity_in=1, arity_out=1, func=toggle_sign, doc='Change sign'),
    'Swap': Operator(opcode='Swap', arity_in=2, arity_out=2, func=swap, doc='Swap two top items in stack'),
    'Drop': Operator(opcode='Drop', arity_in=1, arity_out=0, func=None, doc='Remove the top item from stack'),
}


aliases = {
    'plus': '+', 'KP_Add': '+',
    'minus': '-', 'KP_Subtract': '-',
    'asterisk': '*', 'KP_Multiply': '*',
    'slash': '/', 'KP_Divide': '/',
    'asciicircum': '^',
    'q': WIN_CLOSED, 'Q': WIN_CLOSED, 'Quit': WIN_CLOSED,
    'Return': 'Enter', 'KP_Enter': 'Enter', '\r': 'Enter',
    'Delete': 'Clear', 'c': 'Clear', 'C': 'Clear',
    'D': 'Drop', 'd': 'Drop', 'BackSpace': 'Drop',
    's': 'Swap', 'S': 'Swap',
    'm': '+/-', 'M': '+/-',
    'period': '.', 'KP_Decimal': '.',
    'e': 'E',
    'h': 'Help', 'H': 'Help',
}
