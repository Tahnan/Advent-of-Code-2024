"""
Day 12: Space.  Why did it have to be space?

Determining a region: sure, I can do that, that's just traversing a grid.

Determining the perimeter of the region: all right, I'll have to think about
what constitutes an edge, but sure, I can get there.

Determining the number of sides of a region: please make it stop.

Really, the only good thing going on here is that my debugging for the fifty
line *helper* function worked really well by making it clear how each turn
worked.  Also, super-necessary, because it was so hard for me to visualize.
"""
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


def _turn(inner, outer, direction, turn_is_cw, wall_is_exterior):
    # If we're following an exterior wall, turning clockwise means the inner
    # space is the same and the new outer space is in the direction we're
    # moving, from the inner space. Turning counterclockwise means the *outer*
    # space is the same and the new *inner* space is the direction we're moving,
    # from the *outer* space.
    #
    # And if we're following an interior wall, clockwise has the same *outer*
    # space, counterclockwise has the same *inner* space.  I'd say "trust me,
    # it makes sense", but even I don't trust me that it makes sense.
    if wall_is_exterior == turn_is_cw:
        outer = move(inner, direction)
    else:
        inner = move(outer, direction)
    return inner, outer


def _count_sides(fences, debug=False):
    sides = 0
    wall_is_exterior = True
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
            # otherwise, we'll have to turn CW or CCW.
            new_inner, new_outer = _turn(
                inner, outer, direction, True, wall_is_exterior
            )
            if (new_inner, new_outer) in fences:
                inner, outer = new_inner, new_outer
                direction = turn_cw(direction)
                fences.remove((inner, outer))
                sides += 1
                if debug:
                    print('-CW->', inner, outer)
                continue
            new_inner, new_outer = _turn(
                inner, outer, direction, False, wall_is_exterior
            )
            if (new_inner, new_outer) in fences:
                inner, outer = new_inner, new_outer
                direction = turn_ccw(direction)
                fences.remove((inner, outer))
                sides += 1
                if debug:
                    print('-CCW->', inner, outer)
                continue
            # If neither is a fence, we must have closed the loop
            break
        # Further walls will be exterior walls
        wall_is_exterior = False
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
        (part_two, {'data': TEST_AB}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
