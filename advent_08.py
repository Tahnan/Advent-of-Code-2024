"""
Day 8: Curse this lack of spacial perception!

Well, that was miserable.

On the advice of Denis (https://github.com/denismm/aoc), I finally got around
to writing a vector addition function for my grid util, though I hadn't yet
moved it into this repo.  That's what's below, in move().  So I was all set.
I was even clever enough to add all the points to the set of antinodes and
using & to weed out the ones around the grid later, rather than checking each
antinode for grid membership as I went.

Except that my first attempt:
* had the first coordinate moving in direction * -1, and the second moving in
  direction, because I can't quite ever get my mind around what space means
* had (x1, x2) and (y1, y2) as the coordinates to move from, instead of
  (x1, y1) and (x2, y2).

Debugging that took far, far longer than it should have.  (After which it all
runs in under a second.)
"""

import itertools
from collections import defaultdict
from pathlib import Path

import aoc_util
from grid_util import Grid

TEST_CASE = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".strip()


def move(start, direction, distance=1):
    x, y = start
    dx, dy = direction
    return (x + dx * distance, y + dy * distance)


def parse_data(data):
    return Grid.from_text(data)


def part_one(data=TEST_CASE, debug=False):
    grid = parse_data(data)
    antinodes = set()
    antennae = defaultdict(set)
    for coord, space in grid.items():
        antennae[space].add(coord)
    del antennae['.']
    for ants in antennae.values():
        for (x1, y1), (x2, y2) in itertools.combinations(ants, 2):
            direction = (x1 - x2, y1 - y2)
            antinodes.add(move((x1, y1), direction))
            antinodes.add(move((x2, y2), direction, distance=-1))
    if debug:
        print(antinodes)
    return len(antinodes & grid.keys())


def part_two(data=TEST_CASE, debug=False):
    grid = parse_data(data)
    antinodes = set()
    antennae = defaultdict(set)
    for coord, space in grid.items():
        antennae[space].add(coord)
    del antennae['.']
    for ants in antennae.values():
        for one, two in itertools.combinations(ants, 2):
            (x1, y1), (x2, y2) = one, two
            direction = (x1 - x2, y1 - y2)
            while one in grid:
                antinodes.add(one)
                one = move(one, direction)
            while two in grid:
                antinodes.add(two)
                two = move(two, direction, distance=-1)
    if debug:
        print(antinodes)
    return len(antinodes)


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
