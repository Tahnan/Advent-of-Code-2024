"""
Day 10: Oh for fu--

It took me twenty minutes to figure out what was going wrong.  (I wasn't sure
it was the right approach, but I wanted to stick with it.)  It seemed to be a
good idea to use the "strictly increasing" aspect by doing a breadth-based
search, since you don't have to keep track of the path state: at step 1, you're
moving to height 1; at step 2, to height 2; etc.

And it was great except I got "81" for the test data.  Debug, debug, debug, and
it turns out that because I started with 9 and worked down, I was counting the
ways to get to 9, not the 9s you could get to.  So I redid the whole thing.

And then the test data for part two yielded "81".  Because in fact I had
already solved that part.

Bah.
"""
from collections import Counter
from pathlib import Path

import aoc_util
from grid_util import Grid

TEST_CASE = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""".strip()

DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))


def parse_data(data):
    grid = Grid.from_text(data)
    return Grid({x: int(y) for x, y in grid.items()})


def part_one(data=TEST_CASE, debug=False):
    grid = parse_data(data)
    peaks = {coord: {coord} for coord, content in grid.items() if content == 9}
    for i in range(8, -1, -1):
        all_at_level = set().union(*peaks.values())
        level = {coord: set() for coord in all_at_level}
        for coord, come_from in level.items():
            x, y = coord
            for dx, dy in DIRS:
                neighbor = x + dx, y + dy
                if grid.get(neighbor) == i:
                    come_from.add(neighbor)
        peaks = {coord: set().union(*[level[c] for c in val])
                 for coord, val in peaks.items()}
    return sum([len(c) for c in peaks.values()])


def part_two(data=TEST_CASE, debug=False):
    grid = parse_data(data)
    level = Counter({coord: 1 for coord, content in grid.items()
                     if content == 0})
    for i in range(1, 10):
        new_level = Counter()
        for (x, y), count in level.items():
            for dx, dy in DIRS:
                neighbor = x + dx, y + dy
                if grid.get(neighbor) == i:
                    new_level[neighbor] += count
        level = new_level
    return sum(level.values())


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
