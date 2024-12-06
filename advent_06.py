"""
Day 6: The force, it is *so* brute.

Part one takes under a second.  Part two takes a minute and a half.  I am not
proud of this fact, and I'm going to try to cut that down, but man, brute
force is a powerful drug.
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


def part_one(data=TEST_CASE, debug=False):
    grid = parse_data(data)
    (x, y), = [coord for coord, space in grid.items() if space == '^']
    dx, dy = -1, 0
    visited = set()
    while (x, y) in grid:
        visited.add((x, y))
        forward_space = (x + dx, y + dy)
        if grid.get(forward_space) == '#':
            dx, dy = turn_right(dx, dy)
        else:
            x, y = forward_space
    return len(visited)


def part_two(data=TEST_CASE, debug=False):
    grid = parse_data(data)
    obstacle_helps = 0
    for (ox, oy), space in grid.items():
        if space != '.':
            continue
        new_grid = Grid({**grid, (ox, oy): '#'})
        if grid_is_loop(new_grid):
            obstacle_helps += 1
    return obstacle_helps


def grid_is_loop(grid):
    (x, y), = [coord for coord, space in grid.items() if space == '^']
    dx, dy = -1, 0
    visited = set()
    while (x, y) in grid:
        position = (x, y, dx, dy)
        if position in visited:
            return 1
        visited.add(position)
        forward_space = (x + dx, y + dy)
        if grid.get(forward_space) == '#':
            dx, dy = turn_right(dx, dy)
        else:
            x, y = forward_space
    return 0


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
