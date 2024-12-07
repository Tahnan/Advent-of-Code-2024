"""
Day 7: Not terribly interesting.

A lot not to like about the way this went, such as spending six minutes trying
to debug my code (because itertools.combinations_with_replacement() doesn't
respect order--it returns (add, mul, mul) but not (mul, add, mul) as a
distinct combination--and so I had to switch to itertools.product()).  Or just
copy-pasting part one into part two and changing literally one line.

And...not that interesting a problem?  Maybe there's something other than brute
force (1s on part one, 12s on part two) that would work better, but it's not
apparent to me and brute force worked out just fine.
"""
import itertools
from pathlib import Path

import aoc_util

TEST_CASE = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip()


def parse_data(data):
    lines = [line.split(': ') for line in data.splitlines()]
    return [
        (int(x), [int(z) for z in y.split()]) for x, y in lines
    ]


def add(x, y):
    return x + y


def mul(x, y):
    return x * y


def concat(x, y):
    return int(str(x) + str(y))


def _find_options(data, debug, ops):
    # obviously factored out after finishing
    lines = parse_data(data)
    can_be_done = 0
    for target, numbers in lines:
        options = [ops] * (len(numbers) - 1)
        for operators in itertools.product(*options):
            current, *nums = list(numbers)
            for op, num in zip(operators, nums):
                current = op(current, num)
            if current == target:
                if debug:
                    print(target, numbers, operators, sep='\n')
                can_be_done += target
                break
    return can_be_done


def part_one(data=TEST_CASE, debug=False):
    ops = (add, mul)
    return _find_options(data, debug, ops)


def part_two(data=TEST_CASE, debug=False):
    ops = (add, mul, concat)
    return _find_options(data, debug, ops)


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print(time.ctime(), 'Start')
    for fn, kwargs in (
        (part_one, {'debug': True}),
        (part_one, {'data': DATA}),
        (part_two, {}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
