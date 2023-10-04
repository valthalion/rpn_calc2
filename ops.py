from dataclasses import dataclass
import math
import operator
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
    '+': Operator(opcode='+', arity_in=2, arity_out=1, func=operator.add, doc='Addition'),
    '-': Operator(opcode='-', arity_in=2, arity_out=1, func=operator.sub, doc='Subtraction'),
    '*': Operator(opcode='*', arity_in=2, arity_out=1, func=operator.mul, doc='Multiplication'),
    '/': Operator(opcode='/', arity_in=2, arity_out=1, func=operator.truediv, doc='Division'),
    '^': Operator(opcode='^', arity_in=2, arity_out=1, func=pow, doc='Power'),
    'ln': Operator(opcode='ln', arity_in=1, arity_out=1, func=math.log, doc='Natural logarithm'),
    'exp': Operator(opcode='exp', arity_in=1, arity_out=1, func=math.exp, doc='Exponential function'),
    '2^n': Operator(opcode='2^n', arity_in=1, arity_out=1, func=(lambda n: pow(2, n)), doc='nth power of 2'),
    'log': Operator(opcode='log', arity_in=1, arity_out=1, func=(lambda x: math.log(x, 10)), doc='Base-10 logarithm'),
    'log2': Operator(opcode='log2', arity_in=1, arity_out=1, func=(lambda x: math.log(x, 2)), doc='Base-2 logarithm'),
    'sqrt': Operator(opcode='sqrt', arity_in=1, arity_out=1, func=math.sqrt, doc='Square root'),
    'abs': Operator(opcode='abs', arity_in=1, arity_out=1, func=abs, doc='Absolute value'),
    'floor': Operator(opcode='floor', arity_in=1, arity_out=1, func=math.floor, doc='Floor (round down)'),
    'ceil': Operator(opcode='ceil', arity_in=1, arity_out=1, func=math.ceil, doc='Ceiling (round up)'),
    'mod': Operator(opcode='mod', arity_in=2, arity_out=1, func=operator.mod, doc='Module'),
    'sin': Operator(opcode='sin', arity_in=1, arity_out=1, func=math.sin, doc='Sine'),
    'cos': Operator(opcode='cos', arity_in=1, arity_out=1, func=math.cos, doc='Cosine'),
    'tan': Operator(opcode='tan', arity_in=1, arity_out=1, func=math.tan, doc='Tangent'),
    'asin': Operator(opcode='asin', arity_in=1, arity_out=1, func=math.asin, doc='Arcsine'),
    'acos': Operator(opcode='acos', arity_in=1, arity_out=1, func=math.acos, doc='Arccosine'),
    'atan': Operator(opcode='atan', arity_in=1, arity_out=1, func=math.atan, doc='Arctangent'),
    'inv': Operator(opcode='inv', arity_in=1, arity_out=1, func=(lambda x: 1/x), doc='Inverse (1/x)'),
    'factorial': Operator(opcode='factorial', arity_in=1, arity_out=1, func=(lambda x: math.factorial(int(x))), doc='Factorial (x!)'),
    'pi': Operator(opcode='pi', arity_in=0, arity_out=1, func=(lambda: math.pi), doc='The constant pi'),
    'e_constant': Operator(opcode='e_constant', arity_in=0, arity_out=1, func=(lambda: math.e), doc='The constant e'),
    'R2D': Operator(opcode='R2D', arity_in=1, arity_out=1, func=(lambda x: 180 * x / math.pi), doc='Convert radians to degrees'),
    'D2R': Operator(opcode='D2R', arity_in=1, arity_out=1, func=(lambda x: math.pi * x / 180), doc='Convert degrees to radians'),
    '+/-': Operator(opcode='+/-', arity_in=1, arity_out=1, func=toggle_sign, doc='Change sign'),
    'Swap': Operator(opcode='Swap', arity_in=2, arity_out=2, func=swap, doc='Swap two top items in stack'),
    'Drop': Operator(opcode='Drop', arity_in=1, arity_out=0, func=None, doc='Remove the top item from stack'),
}


aliases = {
    '!': 'factorial',
    '%': 'mod',
    'a': 'abs',
    'c': 'ceil',
    'd': 'R2D',
    'e': 'EEX',
    'f': 'floor',
    'g': 'log',
    'i': 'inv',
    'l': 'ln',
    'm': '+/-',
    'r': 'D2R',
    'p': 'pi',
    's': 'sqrt',
    'x': 'exp',
}

commands = {
    'A': 'Aliases',
    'C': 'Clear',
    'D': 'Drop',
    'E': 'e_constant',
    'H': 'Help',
    'L': 'Load',
    'M': 'Save',
    'S': 'Swap',
    'X': 'ClrMem',
}

other_aliases = {
    'plus': '+', 'KP_Add': '+',
    'minus': '-', 'KP_Subtract': '-',
    'asterisk': '*', 'KP_Multiply': '*',
    'slash': '/', 'KP_Divide': '/',
    'asciicircum': '^',
    'Return': 'Enter', 'KP_Enter': 'Enter', '\r': 'Enter',
    'period': '.', 'KP_Decimal': '.',
    'Delete': 'Clear', 'clear': 'clear',
    'BackSpace': 'Drop', 'drop': 'Drop',
    'swap': 'Swap',
    'Q': WIN_CLOSED, 'Quit': WIN_CLOSED,
    'd2r': 'D2R',
    'r2d': 'R2D',
}

all_aliases = {**aliases, **commands, **other_aliases}
