from pathlib import Path

import aoc_util
from grid_util import Grid

DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))

TEST_CASE = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""".strip()

TEST_E = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""

TEST_AB = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""


def parse_data(data):
    return Grid.from_text(data)


def move(start, direction, distance=1):
    x, y = start
    dx, dy = direction
    return (x + dx * distance, y + dy * distance)


def turn_cw(direction):
    dx, dy = direction
    return dy, -dx


def turn_ccw(direction):
    dx, dy = direction
    return -dy, dx


def _get_regions(farm):
    farm = {**farm}
    regions = []
    while farm:
        coord, crop = farm.popitem()
        this_region = {coord}
        edges = {coord}
        while edges:
            new_edges = set()
            for coord in edges:
                for d in DIRECTIONS:
                    neighbor = move(coord, d)
                    if farm.get(neighbor) == crop:
                        del farm[neighbor]
                        new_edges.add(neighbor)
            edges = new_edges
            this_region.update(edges)
        regions.append(this_region)
    return regions


def _get_perimeter(region):
    fences = 0
    for coord in region:
        for d in DIRECTIONS:
            if move(coord, d) not in region:
                fences += 1
    return fences


def _get_sides(region, debug=False):
    # this is a mess
    # "fences" is (coord_i, coord_o), where coord_i is inside the region and
    # coord_o is outside the region
    fences = set()
    for coord in region:
        for d in DIRECTIONS:
            other = move(coord, d)
            if other not in region:
                fences.add((coord, other))
    if debug:
        print('>', fences)
    return _count_sides(fences)


def _count_sides(fences, debug=False):
    sides = 0
    while fences:
        inner, outer = min(fences)
        direction = (0, 1)
        if debug:
            print('START:', inner, outer)
        fences.remove((inner, outer))
        sides += 1
        while True:
            new_inner = move(inner, direction)
            new_outer = move(outer, direction)
            # if we can continue in this direction, cool
            if (new_inner, new_outer) in fences:
                inner, outer = new_inner, new_outer
                fences.remove((inner, outer))
                if debug:
                    print('-->', inner, outer)
                continue
            # otherwise, we'll have to turn CW or CCW.  Because we're following
            # the "left" wall, turning clockwise means the inner space is the
            # same and the new outer space is in the direction we're moving,
            # from the inner space. Turning coutnerclockwise means the *outer*
            # space is the same and the new *inner* space is the direction
            # we're moving, from the *outer* space.
            cw_outer = move(inner, direction)
            if (inner, cw_outer) in fences:
                outer = cw_outer
                direction = turn_cw(direction)
                fences.remove((inner, outer))
                sides += 1
                if debug:
                    print('-CW->', inner, outer)
                continue
            ccw_inner = move(outer, direction)
            if (ccw_inner, outer) in fences:
                inner = ccw_inner
                direction = turn_ccw(direction)
                fences.remove((inner, outer))
                sides += 1
                if debug:
                    print('-CCW->', inner, outer)
                continue
            # If neither is a fence, we must have closed the loop
            break
    return sides


def part_one(data=TEST_CASE, debug=False):
    farm = parse_data(data)
    regions = _get_regions(farm)
    cost = 0
    for region in regions:
        perimeter = _get_perimeter(region)
        cost += perimeter * len(region)
        if debug:
            print(farm[min(region)], len(region), perimeter)
    return cost


def part_two(data=TEST_CASE, debug=False):
    # First guess: 839873, too high
    farm = parse_data(data)
    regions = _get_regions(farm)
    cost = 0
    for region in regions:
        sides = _get_sides(region, debug=debug)
        cost += sides * len(region)
        if debug:
            print(farm[min(region)], len(region), sides)
    return cost


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
        (part_two, {'data': TEST_E}),
        (part_two, {'data': TEST_AB, 'debug': True}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
