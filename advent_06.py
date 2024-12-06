"""
Day 6: The force, it is *so* brute.

Part one takes under a second.  Part two takes a minute and a half.  I am not
proud of this fact, and I'm going to try to cut that down, but man, brute
force is a powerful drug.

EDIT: with the revisions here, part two takes nine seconds.  It turns out that
you don't have to check every space in the grid, just the spaces the guard
visits.  (It also helps to calculate start once, rather than once per
traversal.)  That cuts the runs to check from 16,071 (the number of empty
spaces in the input) to 5101 (the number of spaces traversed in part one), to
say nothing of the fact that those other 11k spaces were over 5000 moves each.

What really made the difference, of course, was being able to factor out
traverse_grid(), so that part two could *get* the spaces the guard visits.
Brute force is a powerful drug, kids, but it doesn't hold a candle to careful
design and factoring out common code.  Stay in school.
"""

from pathlib import Path

import aoc_util
from grid_util import Grid

TEST_CASE = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".strip()


def turn_right(dx, dy):
    return dy, -dx


def parse_data(data):
    return Grid.from_text(data)


def traverse_grid(grid, start):
    x, y = start
    dx, dy = -1, 0
    visited = set()
    while (x, y) in grid:
        position = (x, y, dx, dy)
        if position in visited:
            return  # there's a loop
        visited.add(position)
        forward_space = (x + dx, y + dy)
        if grid.get(forward_space) == '#':
            dx, dy = turn_right(dx, dy)
        else:
            x, y = forward_space
    return {(x, y) for x, y, _, _ in visited}


def part_one(data=TEST_CASE, debug=False):
    grid = parse_data(data)
    start, = [coord for coord, space in grid.items() if space == '^']
    visited = traverse_grid(grid, start)
    return len(visited)


def part_two(data=TEST_CASE, debug=False):
    grid = parse_data(data)
    start, = [coord for coord, space in grid.items() if space == '^']
    visited = traverse_grid(grid, start)

    obstacle_helps = 0
    for space in visited:
        new_grid = Grid({**grid, space: '#'})
        if traverse_grid(new_grid, start) is None:
            obstacle_helps += 1
    return obstacle_helps


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
