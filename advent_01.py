"""
Day 1: Ugh, right, speed-coding.

I'm not *really* going for speed, not in an event where the first person
finished the first puzzle in 4 seconds, and the second part five seconds
later.  Doing part two in 5:09 got me 815th.  So, right, forget the speed.

Even so, this was a simple little task that took three and a half minutes
because I kept screwing up the data parsing: forgetting that the elements of
zip() were tuples and not lists; forgetting to convert their contents to
integers...well, whatever.  Nothing interesting enough in the task to warrant
comment.
"""

from pathlib import Path

import aoc_util

TEST_CASE = """3   4
4   3
2   5
1   3
3   9
3   3""".strip()


def parse_data(data):
    one, two = zip(*[line.split() for line in data.strip().splitlines()])
    one = [int(x) for x in one]
    two = [int(x) for x in two]
    return one, two


def part_one(data=TEST_CASE, debug=False):
    one, two = parse_data(data)
    one.sort()
    two.sort()
    return sum(abs(x - y) for x, y in zip(one, two))


def part_two(data=TEST_CASE, debug=False):
    one, two = parse_data(data)
    return sum(two.count(n) * n for n in one)


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
