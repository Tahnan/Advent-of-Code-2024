"""
Day 14: what

Part 1 shouldn't have taken as long as it did; I think it was just a couple of
little debugging things.  Well, you can see what kind of debugging I needed.

Part 2...I can only assume I did this right.  I'm not positive what you *can*
do other than inspect the robot positions, and "most of them" forming a
"Christmas tree" is very vague.  I started--well, I started by missing "most"
and looking to see if they were *all* connected, but once that was out of the
way, I did a debugging check by printing their locations when at least half of
them were adjacent to another robot; I tried it at .9, but didn't get any
results; I lowered it to .7 and, sure enough, the first result it printed had
a tree in it.

Weird though.
"""
from collections import Counter
from pathlib import Path

import aoc_util
from grid_util import DIRECTIONS

TEST_CASE = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""".strip()


def move_wrapped(start, direction, size, distance=1):
    sx, sy = size
    x, y = start
    dx, dy = direction
    return (x + dx * distance) % sx, (y + dy * distance) % sy


def parse_data(data):
    robots = []
    for line in data.splitlines():
        p, v = line.split()
        p = [int(x) for x in p[2:].split(',')]
        v = [int(x) for x in v[2:].split(',')]
        robots.append((p, v))
    return robots


def _parse_quadrants(coords, size):
    sx, sy = size
    half_x = (sx - 1) // 2
    half_y = (sy - 1) // 2
    quadrants = Counter()
    for x, y in coords:
        if x == half_x or y == half_y:
            continue
        quadrants[x < half_x, y < half_y] += 1
    return quadrants


def test_robot_one():
    p = (2, 4)
    v = (2, -3)
    for d in range(6):
        print(move_wrapped(p, v, (11, 7), distance=d), end=' ')
    print()


def part_one(data=TEST_CASE, debug=False):
    if data == TEST_CASE:
        space = (11, 7)
    else:
        space = (101, 103)
    robots = parse_data(data)
    final_locations = [
        move_wrapped(start, direction, space, distance=100)
        for start, direction in robots
    ]
    if debug:
        print(sorted(final_locations))
    quads = _parse_quadrants(final_locations, space)
    if debug:
        print(quads)
    factor = 1
    for quad in quads.values():
        factor *= quad
    return factor


def has_neighbor(coord, locations):
    for d in DIRECTIONS:
        if move_wrapped(coord, d, (1000, 1000)) in locations:
            return True
    return False


def part_two(data=TEST_CASE, debug=False):
    # I'm sorry what
    robots = parse_data(data)
    moves = 0
    while True:
        moves += 1
        robots = [(move_wrapped(p, v, (101, 103)), v) for p, v in robots]
        locations = {p for p, v in robots}
        in_a_shape = sum(has_neighbor(c, locations) for c in locations)
        if in_a_shape / len(locations) > .7:
            print(moves)
            for row in range(103):
                for column in range(101):
                    print('*' if (column, row) in locations else '-', end='')
                print()
            print()
            if input('>'):
                return moves


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    test_robot_one()
    print(time.ctime(), 'Start')
    for fn, kwargs in (
        (part_one, {'debug': True}),
        (part_one, {'data': DATA}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
