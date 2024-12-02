"""
Day 2: Hooray refactoring!

Because speed coding, "is_it_safe" started out inlined in part_one(), with
"break" instead of "return" as oppropriate.  Then of course it got factored
out for part two.

Part two does work better with none of the lists being terribly long, such
that it's sufficiently efficient to just try deleting each element to see
whether it makes the list safe.  (Breaking out of the loop as soon as one is
found, of course, helps, but not if the answer is "no".)  Possibly the whole
check is fast enough that it wouldn't matter even if it were a much longer
list?  Checking while proceeding through the list seems possible but less
pleasant.

Also, thank god I learned about itertools.pairwise() between last year and now.
"""
import itertools
from pathlib import Path

import aoc_util

TEST_CASE = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""".strip()


def parse_data(data):
    return [[int(x) for x in line.split()] for line in data.splitlines()]


def is_it_safe(report):
    order = sorted(report)
    if order != report and order != report[::-1]:
        return False
    for a, b in itertools.pairwise(report):
        if not (1 <= abs(a - b) <= 3):
            return False
    return True


def part_one(data=TEST_CASE, debug=False):
    reports = parse_data(data)
    safe = 0
    for report in reports:
        if is_it_safe(report):
            safe += 1
    return safe


def part_two(data=TEST_CASE, debug=False):
    reports = parse_data(data)
    safe = 0
    for report in reports:
        if is_it_safe(report):
            safe += 1
            continue
        for i in range(len(report)):
            if is_it_safe(report[:i] + report[i + 1:]):
                safe += 1
                break
    return safe


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
