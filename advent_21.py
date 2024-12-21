import itertools

from grid_util import move, NORTH, SOUTH, EAST, WEST
from pathlib import Path

import aoc_util

DIRECTIONS = {NORTH: '^', SOUTH: 'v', WEST: '<', EAST: '>'}

# KEYPAD:
# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

KEYPAD = {'7': (0, 0), '8': (0, 1), '9': (0, 2),
          '4': (1, 0), '5': (1, 1), '6': (1, 2),
          '1': (2, 0), '2': (2, 1), '3': (2, 2),
                       '0': (3, 1), 'A': (3, 2)}

# ROBOT:
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

ROBOT = {
                 '^': (0, 1), 'A': (0, 2),
    '<': (1, 0), 'v': (1, 1), '>': (1, 2)
}

TEST_CASE = """
029A
980A
179A
456A
379A
""".strip()

# Answers:
# 029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
# 980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
# 179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
# 456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
# 379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A


def get_moves(code, pad):
    code = list(code)
    buttons = []
    for from_button, to_button in itertools.pairwise(['A'] + code):
        (fx, fy), (tx, ty) = pad[from_button], pad[to_button]
        ns = NORTH if fx > tx else SOUTH
        ew = WEST if fy > ty else EAST
        buttons.extend([DIRECTIONS[ns]] * abs(fx - tx))
        buttons.extend([DIRECTIONS[ew]] * abs(fy - ty))
        buttons.append('A')
    return buttons


def type_code(code, debug=False):
    inner = get_moves(code, KEYPAD)
    middle = get_moves(inner, ROBOT)
    outer = get_moves(middle, ROBOT)
    if debug:
        print(''.join(outer))
        print(''.join(middle))
        print(''.join(inner))
        print(code)
    return outer


def complexity(code, buttons):
    return int(code[:-1]) * len(buttons)


def part_one(data=TEST_CASE, debug=False):
    codes = data.split()
    total = 0
    for code in codes:
        buttons = type_code(code)
        total += complexity(code, buttons)
    return total


def part_two(data=TEST_CASE, debug=False):
    pass


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print(time.ctime(), 'Start')
    for fn, kwargs in (
        (type_code, {'code': '029A', 'debug': True}),
        (part_one, {}),
        (part_one, {'data': DATA}),
        (part_two, {}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
