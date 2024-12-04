"""
Day 4: Oh crap, it's 12:07!

Darn it, Stephen Colbert, you totally distracted me and I forgot to watch the
clock.  Why do I do time-based competitive things?

The initial puzzles each year are pretty straightforward, but even so I admit
I'm hoping the challenge starts ramping up a little.  Of course, the fact that
I have a Grid class onhand does mean that grid-searching in particular isn't
going to feel new and exciting.
"""
from pathlib import Path

import aoc_util
from grid_util import Grid

TEST_CASE = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".strip()

DIAGONALS = (((-1, -1), (1, 1)), ((-1, 1), (1, -1)))


def parse_data(data):
    return Grid.from_text(data)


def part_one(data=TEST_CASE, debug=False):
    # OK, I skipped this part because I already have a program to solve word
    # searches, so I just dumped the grid into that and searched for "XMAS" and
    # it told me how many times it occurs
    pass


def part_two(data=TEST_CASE, debug=False):
    grid = parse_data(data)
    count = 0
    for coord, content in grid.items():
        if content != 'A':
            continue
        if coord[0] in (0, grid.rows - 1) or coord[1] in (0, grid.columns - 1):
            continue
        x, y = coord
        diagonals = [
            {grid[(x - dx, y - dy)] for dx, dy in adjacent}
            for adjacent in DIAGONALS
        ]
        if diagonals == [{'M', 'S'}, {'M', 'S'}]:
            count += 1
    return count



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
