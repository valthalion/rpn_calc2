"""
An RPN Calculator
"""


from itertools import chain
from sys import argv
from typing import Any, Iterable, List, Optional, Tuple, Union

import PySimpleGUI as sg

from ops import aliases, operators
from stack import Stack
from errors import NotEnoughArgumentsError


################################################################################
# Initial Definitions

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


sg.theme('DarkGrey13')
sg.set_options(element_padding=(0, 0))


################################################################################
# Read options and set parameters

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


def pprint_stack(stack: Stack) -> str:
    index_width = 1 + (display_size // 10)
    number_width = text_width - (index_width + 2)  # reserve space for index + ': '

    if len(stack) >= display_size:
        return '\n'.join(
            f'{row:>{index_width}d}: {number:>{number_width}g}'
            for row, number in zip(range(display_size, 0, -1), stack[-display_size:])
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


################################################################################
# Declare GUI items

stack = Stack()
edit_line = ''

error_display = sg.Text(
    '',
    key='error_display',
    size=(text_width, 1),
    font=('Fira Code', text_size),
    text_color='red',
    pad=(0, 3),
    justification='l',
)

stack_display = sg.Text(
    pprint_stack(stack),
    key='stack',
    size=(text_width, display_size),
    font=('Fira Code', text_size),
    pad=(0, 3),
)

edit_line_display = sg.Text(
    edit_line,
    key='edit_line',
    size=(text_width, 1),
    font=('Fira Code', text_size),
    pad=(0, 3),
    justification='r',
)


################################################################################
# Specify layout & create window

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
   # no_titlebar=True,
   default_button_element_size=button_size,
   auto_size_buttons=False,
   grab_anywhere=True,
   keep_on_top=keep_on_top,
   finalize=True,
)
window.bind('<Key>', 'Key')


################################################################################
# Event loop

while True:
    event, values = window.read()

    # Key pressed: retrieve key value
    if event == 'Key':
        event = str(window.user_bind_event.keysym)
        # Strip 'KP_' prefix from num pad numbers -> same as normal number keys
        if len(event) == 4 and event.startswith('KP_'):
            event = event[-1]

    # Check if the event is an alias and set the cannonical value
    event = aliases.get(event, event)

    if event == sg.WIN_CLOSED:
        break

    # Start event evaluation (note if, elif, ... structure if adding more)

    if event == 'Enter':
        if edit_line:
            if edit_line.endswith('e') or edit_line.endswith('e-'):  # Drop trailing 'e' or 'e-', assume equvalent to e0
                edit_line = edit_line.split('e')[0]
            stack.push(float(edit_line))
            edit_line = ''
            window['edit_line'].update(edit_line)
            window['stack'].update(pprint_stack(stack))

    elif event == 'Clear':
        if edit_line:  # if editing, delete edit line
            edit_line = ''
            window['edit_line'].update(edit_line)
        else:  # clear the stack
            stack.clear()
            window['stack'].update(pprint_stack(stack))

    elif event == 'Drop' and edit_line:  # if not editing, will be interpreted later as an operator
        if edit_line:  # if editing, delete last character
            edit_line = edit_line[:-1]
            window['edit_line'].update(edit_line)
        else:  # drop top stack item
            evaluate(event)

    elif event == '+/-' and edit_line:  # if not editing, will be interpreted later as an operator
        if 'e' in edit_line:  # if editing the exponent, toggle exponent sign
            base, exp = edit_line.split('e')
            edit_line = 'e'.join((base, toggle_sign(exp)))
        else:  # toggle mantissa sign
            edit_line = toggle_sign(edit_line)
        window['edit_line'].update(edit_line)

    elif event == '.':
        if '.' in edit_line:
            window['error_display'].update('Only one point allowed')
            continue
        edit_line = f'{edit_line}.'
        window['edit_line'].update(edit_line)

    elif event == 'E':
        if 'e' in edit_line:
            window['error_display'].update('Only one "e" allowed')
            continue
        if edit_line:
            edit_line = f'{edit_line}e'
        else:  # empty line -> interpret as 1e
            edit_line = '1e'
        window['edit_line'].update(edit_line)

    elif event in '0123456789':
        edit_line = f'{edit_line}{event}'
        window['edit_line'].update(edit_line)

    elif event in operators:
        if edit_line:  # if editing, push to stack before operating; taken from Enter event
            if edit_line.endswith('e'):  # Drop trailing 'e', assume equvalent to e0
                edit_line = edit_line[:-1]
            stack.push(float(edit_line))
            edit_line = ''
            window['edit_line'].update(edit_line)
            window['stack'].update(pprint_stack(stack))
        operator = operators[event]
        try:
            args = stack.pop_iter(operator.arity_in)
        except NotEnoughArgumentsError:
            window['error_display'].update('Too few arguments')
            continue
        if operator.func is not None:
            try:
                result = operator.func(*args)
            except Exception as e:
                window['error_display'].update(str(e))
                for arg in args:
                    stack.push(arg)
                continue
        if operator.arity_out == 1:
            stack.push(result)
        elif operator.arity_out > 1:
            stack.push_iter(result)
        else:  # arity_out == 0
            pass
        window['stack'].update(pprint_stack(stack))

    elif event == 'Help':
        sg.popup(help_text)

    else:
        #print('WTF:', event, values)
        pass

    window['error_display'].update('')

window.close()
