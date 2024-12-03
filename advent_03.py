"""
Day 3: And now I have two problems.

Regular expressions were the right way to solve this, except that every time I
have to look up the documentation--not of regexes, just of the "re" module to
remind me that findall() returns groups and finditer() returns match objects
that have a groups() method except that it has None where the findall() groups
have an empty string and--

Well, whatever, it's over now.
"""
import re
from pathlib import Path

import aoc_util

TEST_CASE = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
""".strip()

MUL_RE = re.compile(r'mul\(([0-9]+),([0-9]+)\)')

NEW_MUL_RE = re.compile(r'mul\(([0-9]+),([0-9]+)\)|do(n\'t)?\(\)')


def part_one(data=TEST_CASE, debug=False):
    total = 0
    for mult in MUL_RE.finditer(data):
        a, b = mult.groups()
        total += int(a) * int(b)
    return total


def part_two(data=TEST_CASE, debug=False):
    total = 0
    dont = False
    for mult in NEW_MUL_RE.finditer(data):
        groups = mult.groups()
        if groups == (None, None, None):
            dont = False
        elif groups == (None, None, "n't"):
            dont = True
        elif not dont:
            a, b, _ = groups
            total += int(a) * int(b)
    return total


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print(time.ctime(), 'Start')
    for fn, kwargs in (
        (part_one, {}),
        (part_one, {'data': DATA}),
        (part_two, {}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
