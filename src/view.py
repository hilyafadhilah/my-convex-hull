#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""View module for Find Convex Hull program

Notes
-----
Comments are omitted because code is self-explanatory.
"""

colors = [
    'aquamarine',
    'azure',
    'blue',
    'brown',
    'chartreuse',
    'chocolate',
    'coral',
    'crimson',
    'cyan',
    'darkblue',
    'darkgreen',
    'fuchsia',
    'gold',
    'green',
    'grey',
    'indigo',
    'khaki',
    'lavender',
    'lightblue',
    'lightgreen',
    'lime',
    'magenta',
    'maroon',
    'navy',
    'olive',
    'orange',
    'orangered',
    'orchid',
    'pink',
    'plum',
    'purple',
    'red',
    'salmon',
    'sienna',
    'tan',
    'teal',
    'tomato',
    'turquoise',
    'violet',
    'wheat',
    'yellow',
    'yellowgreen',
]

colors = list(map(lambda x: f"xkcd:{x}", colors))

def displayHeader(title: str) -> None:
    n = (60 - len(title) - 4) // 2

    if n > 0:
        header = f"\n {'=' * n} {title} {'=' * n}\n"
    else:
        header = f"\n {title}\n"

    print(header)

def displayList(lst: list, key = None) -> None:
    maxSpace = len(str(len(lst)))
    for i in range(len(lst)):
        x = lst[i][key] if key else lst[i]
        spacing = maxSpace - len(str(i + 1)) + 4
        print(f"{' ' * spacing}{i + 1}. {x}")
    print('')

def toTitle(label: str) -> str:
    return label.replace('_', ' ').title()

def inputInt(prompt: str, minval: int = None, maxval: int = None, exclude: list = None) -> int:
    while True:
        try:
            inp = int(input(prompt + " "))

            if (minval is not None and inp < minval) or (maxval is not None and inp > maxval):
                print(f"Number must be between {minval} and {maxval}.")
                raise Exception

            if exclude is not None and inp in exclude:
                print(f"Number cannot be {inp}.")
                raise Exception

            return inp
        except ValueError:
            print("Invalid number.")
        except Exception:
            pass
