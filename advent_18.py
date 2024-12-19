"""
Day 18: More mazes!

Really, the hardest part was getting it wrong twice because I submitted
"(X, Y)" with the parentheses and then "X, Y" with a space in it.  Oh well.

Kind of wish I had been able to do this in real time.  Alas, serious headache
knocked me flat well before midnight.
"""

from pathlib import Path

import aoc_util
from grid_util import CARDINALS, DIRECTIONS, move

TEST_CASE = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
""".strip()


def parse_data(data):
    return [tuple([int(c) for c in line.split(',')])
            for line in data.splitlines()]


def in_bounds(coord, size):
    x, y = coord
    return 0 <= x <= size and 0 <= y <= size


def part_one(data=TEST_CASE, debug=False):
    coords = parse_data(data)
    size = 6 if data == TEST_CASE else 70
    corrupted = coords[:12 if data == TEST_CASE else 1024]

    # god, we're traversing a maze *again*?
    current = {(0, 0)}
    do_not_move_to = {(0, 0), *corrupted}
    end = (size, size)
    steps = 0
    while True:
        steps += 1
        new = set()
        for coord in current:
            for direction in CARDINALS:
                neighbor = move(coord, direction)
                if neighbor == end:
                    return steps
                if neighbor in do_not_move_to:
                    continue
                if not in_bounds(neighbor, size):
                    continue
                new.add(neighbor)
        current = new


def coord_is_lower_left(coord, size):
    return coord[0] == 0 or coord[1] == size


def coord_is_upper_right(coord, size):
    return coord[1] == 0 or coord[0] == size


def part_two(data=TEST_CASE, debug=False):
    # You know what's faster than traversing a maze?  Looking to see whether
    # two sections of walls are connected.  OK, that's still technically
    # traversing a maze, but it's got fewer coordinates in it.
    coords = parse_data(data)
    size = 6 if data == TEST_CASE else 70

    # We know there's a path through the first 12 or 1024, so we don't need
    # to check those
    cutoff = 12 if data == TEST_CASE else 1024
    corrupted, remainder = coords[:cutoff], coords[cutoff:]
    corrupted = set(corrupted)
    remainder.reverse()
    lower_left = {c for c in corrupted if coord_is_lower_left(c, size)}
    upper_right = {c for c in corrupted if coord_is_upper_right(c, size)}

    while True:
        new_coord = remainder.pop()
        if coord_is_lower_left(new_coord, size):
            lower_left.add(new_coord)
        if coord_is_upper_right(new_coord, size):
            upper_right.add(new_coord)
        corrupted.add(new_coord)

        current = lower_left
        visited = {*current}
        while current:
            new = set()
            for coord in current:
                for direction in DIRECTIONS:
                    neighbor = move(coord, direction)
                    if neighbor in upper_right:
                        return new_coord
                    if neighbor in visited or neighbor not in corrupted:
                        continue
                    new.add(neighbor)
            current = new
            visited.update(current)


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
