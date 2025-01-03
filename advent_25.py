"""
Day 25: 360th? Really?

I kind of stumbled through this--I kept checking that everything was size 5,
I had to go back and subtract one in parse_data because I was counting the
top/bottom row...and really in the end it was just "check everything against
everything", nothing terribly clever.  Did not expect to be in the top
thousand for that solution.

Meanwhile, of course, I'm six stars short of part 2.
"""
from pathlib import Path

import aoc_util

TEST_CASE = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
""".strip()


def parse_data(data):
    keys = []
    locks = []
    for group in data.split('\n\n'):
        cols = [col.count('#') - 1 for col in zip(*group.splitlines())]
        top_row = set(group.splitlines()[0])
        if top_row == {'#'}:
            locks.append(cols)
        elif top_row == {'.'}:
            keys.append(cols)
        else:
            raise RuntimeError('What!?')
    return locks, keys


def part_one(data=TEST_CASE, debug=False):
    keys, locks = parse_data(data)
    fits = 0
    for key in keys:
        for lock in locks:
            if all(k + l <= 5 for k, l in zip(key, lock)):
                fits += 1
    return fits


def part_two(data=TEST_CASE, debug=False):
    return 'I do not yet have 49 stars.'  # presumably this is part 2


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
