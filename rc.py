"""
An RPN Calculator
"""


from itertools import chain
# from math import sqrt, sin, cos, tan
from operator import add, mul, sub, truediv
from sys import argv
from typing import Any, Iterable, List, Optional, Tuple, Union

import PySimpleGUI as sg
sg.theme('DarkGrey13')
sg.set_options(element_padding=(0, 0))


class NotEnoughArgumentsError(RuntimeError):
    pass


op = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '^': pow
}


options = '' if len(argv) <= 1 else argv[1]
if 'l' in options:
    button_size = (9, 3)
    text_size = 16
elif 's' in options:
    button_size = (5, 2)
    text_size = 10
else:
    button_size = (8, 2)
    text_size = 14
keep_on_top = 't' in options
display_size = 4
text_width = 22

help_text = """
Keyboard uses the same keys as
the GUI buttons, and these aliases:

Quit: q
Drop: d, Backspace
Clear: c, Del
Swap: s
+/-: m

All commands are case-insensitive.
"""


def toggle_sign(num):
    if num.startswith('-'):
        return num[1:]
    return f'-{num}'


class Stack:
    def __init__(self) -> None:
        self._stack: List = []

    def __bool__(self):
        return len(self._stack) > 0

    def __len__(self):
        return len(self._stack)

    def __iter__(self):
        return iter(self._stack)

    def push(self, value: Any) -> None:
        self._stack.append(value)

    def pop(self, n: int = 1) -> Union[Tuple, Any]:
        if len(self._stack) < n:
            raise NotEnoughArgumentsError(self, n)
        if n == 1:
            return self._stack.pop()
        self._stack, result = self._stack[:-n], self._stack[-n:]
        return tuple(result)

    def swap(self):
        if len(self._stack) < 2:
            raise NotEnoughArgumentsError('Too few arguments')
        self._stack[-1], self._stack[-2] = self._stack[-2], self._stack[-1]

    def clear(self) -> None:
        self._stack = []




def pprint_stack(stack) -> str:
    index_width = 1 + (display_size // 10)
    number_width = text_width - (index_width + 2)  # reserve space for index + ': '

    if len(stack) >= display_size:
        return '\n'.join(
            f'{row:>{index_width}d}: {number:>{number_width}g}'
            for row, number in zip(range(display_size, 0, -1), stack[display_size:])
            )

    stack_len = len(stack)
    return '\n'.join(
        chain(
            (
                ': '.join((f'{row:>{index_width}d}', ' ' * number_width))
                for row in range(display_size, stack_len, -1)
            ),
            (
                f'{row:>{index_width}d}: {number:>{number_width}g}'
                for row, number in zip(range(stack_len, 0, -1), stack)
            )
        )
    )


stack = Stack()
edit_line = ''

error_display = sg.Text('', key='error_display', size=(text_width, 1), font=('Fira Code', text_size), text_color='red', pad=(0, 3), justification='l')
stack_display = sg.Text(pprint_stack(stack), key='stack', size=(text_width, display_size), font=('Fira Code', text_size), pad=(0, 3))
edit_line_display = sg.Text(edit_line, key='edit_line', size=(text_width, 1), font=('Fira Code', text_size), pad=(0, 3), justification='r')

layout = [
    [error_display],
    [stack_display],
    [edit_line_display],
    [sg.Button('Clear'), sg.Button('Drop'), sg.Button('Swap'), sg.Button('Quit', button_color=('white', 'red'))],
    [sg.Button('7'), sg.Button('8'), sg.Button('9'), sg.Button('/')],
    [sg.Button('4'), sg.Button('5'), sg.Button('6'), sg.Button('*')],
    [sg.Button('1'), sg.Button('2'), sg.Button('3'), sg.Button('-')],
    [sg.Button('E'), sg.Button('0'), sg.Button('.'), sg.Button('+')],
    [sg.Button('Enter'), sg.Button('+/-'), sg.Button('Help'), sg.Button('^')]
]

window = sg.Window(
   'RPN Calculator', layout,
   no_titlebar=True,
   return_keyboard_events=True,
   default_button_element_size=button_size,
   auto_size_buttons=False,
   grab_anywhere=True,
   keep_on_top=keep_on_top,
)

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Q', 'q', 'Quit'):
        break

    if event in ('Enter', '\r'):
        if edit_line:
            if edit_line.endswith('e'):
                edit_line = edit_line[:-1]
            stack.push(float(edit_line))
            edit_line = ''
            window['edit_line'].update(edit_line)
            window['stack'].update(pprint_stack(stack))

    elif event in ('Delete:46', 'c', 'C', 'Clear'):
        edit_line = ''
        stack.clear()
        window['edit_line'].update(edit_line)
        window['stack'].update(pprint_stack(stack))

    elif event in ('Drop', 'D', 'd', 'BackSpace:8'):
        if edit_line:
            edit_line = edit_line[:-1]
            window['edit_line'].update(edit_line)
        else:
            if not stack:
                window['error_display'].update('Too few arguments')
                continue
            stack.pop()
            window['stack'].update(pprint_stack(stack))

    elif event in ('Swap', 'S', 's'):
        if edit_line:
            window['error_display'].update('No swap while editing')
            continue
        try:
            stack.swap()
        except NotEnoughArgumentsError as e:
            window['error_display'].update(str(e))
            continue
        window['stack'].update(pprint_stack(stack))

    elif event in ('+/-', 'M', 'm'):
        if 'e' in edit_line:
            base, exp = edit_line.split('e')
            edit_line = 'e'.join((base, toggle_sign(exp)))
        else:
            edit_line = toggle_sign(edit_line)
        window['edit_line'].update(edit_line)

    elif event == '.':
        if '.' in edit_line:
            window['error_display'].update('Only one point allowed')
            continue
        edit_line = f'{edit_line}.'
        window['edit_line'].update(edit_line)

    elif event in 'Ee':
        if 'e' in edit_line:
            window['error_display'].update('Only one "e" allowed')
            continue
        edit_line += 'e'
        window['edit_line'].update(edit_line)

    elif event in '0123456789':
        edit_line += event
        window['edit_line'].update(edit_line)

    elif event in op:
        if edit_line:
            stack.push(float(edit_line))
            edit_line = ''
        window['edit_line'].update(edit_line)
        window['stack'].update(pprint_stack(stack))
        try:
            args = stack.pop(2)
        except NotEnoughArgumentsError:
            window['error_display'].update('Too few arguments')
            continue
        try:
            result = op[event](*args)
        except Exception as e:
            window['error_display'].update(str(e))
            for arg in args:
                stack.push(arg)
            continue
        stack.push(result)
        window['stack'].update(pprint_stack(stack))

    elif event in ('Help', 'H', 'h'):
        sg.popup(help_text)

    else:
        #print('WTF:', event, values)
        pass

    window['error_display'].update('')

window.close()
