"""
Day 20: The maze, eet ees too much

Either I'm worn out, or this problem wore me out.  I was basically trudging
through molasses to get this done, and felt like I was keeping track of all the
wrong things along the way.  It took almost half an hour (and 1214th isn't my
worst showing on part one, but it's nothing exciting).

I feel like I know how I want to approach part two, but I also feel like I want
to lie down and sleep even more.  So I'm punting until tomorrow.

---

Tomorrow: oh god why does my test pass but the real data fails
"""
from collections import Counter
from pathlib import Path

import aoc_util
from grid_util import Grid, CARDINALS, move

TEST_CASE = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
""".strip()


def parse_data(data):
    return Grid.from_text(data)


def get_coord_to_remainder(grid, start, end):
    walls = {coord for coord, content in grid.items() if content == '#'}
    # length of path should be grid_size - walls - 1 (for start; end is on path)
    distance_to_end = len(grid) - len(walls) - 1
    distances = {start: distance_to_end}
    location = start
    while location != end:
        distance_to_end -= 1
        location = get_only_move(location, walls | distances.keys())
        distances[location] = distance_to_end
    assert distance_to_end == 0
    return distances


def get_only_move(location, blocked):
    possible = {
        direction for direction in CARDINALS
        if move(location, direction) not in blocked
    }
    assert len(possible) == 1
    direction, = possible
    return move(location, direction)


def part_one(data=TEST_CASE, debug=False):
    grid = parse_data(data)
    max_r, max_c = max(grid)
    start, = {coord for coord, content in grid.items() if content == 'S'}
    end, = {coord for coord, content in grid.items() if content == 'E'}
    distances_to_end = get_coord_to_remainder(grid, start, end)
    cheats = Counter()
    location = start

    while location != end:
        time_from_loc = distances_to_end[location]
        glitch_locs = []
        new_location = None
        for direction in CARDINALS:
            nx, ny = move(location, direction)
            contents = grid[(nx, ny)]
            if contents == '#':
                if nx not in (0, max_r) and ny not in (0, max_c):
                    glitch_locs.append((nx, ny))
            elif distances_to_end[(nx, ny)] < time_from_loc:
                new_location = (nx, ny)
        for glitch in glitch_locs:
            for direction in CARDINALS:
                other_side = move(glitch, direction)
                if grid[other_side] == '#' or other_side == location:
                    continue
                # We're on the other side.  How much time did we save?
                time_from_here = distances_to_end[other_side]
                time_saved = time_from_loc - time_from_here - 2
                if time_saved > 0:
                    cheats[time_saved] += 1
        location = new_location
        if location is None:
            raise RuntimeError('Crash!')
    return sum(count for time_saved, count in cheats.items()
               if time_saved >= 100)


def generate_coordinates_at_distance(coord, distance=20):
    """
    Given a coordinate and (optionally) a distance, generate all coordinates
    within that (Manhattan) distance.
    """
    for x in range(-distance, distance + 1):
        perpendicular = abs(distance) - x
        for y in range(-perpendicular, perpendicular + 1):
            yield move(coord, (x, y)), abs(x) + abs(y)


# 2072373 is too high - though the test case passes!
def part_two(data=TEST_CASE, debug=False):
    # Throw all of that out and start over
    grid = parse_data(data)
    start, = {coord for coord, content in grid.items() if content == 'S'}
    end, = {coord for coord, content in grid.items() if content == 'E'}
    distances_to_end = get_coord_to_remainder(grid, start, end)
    cheats = Counter()
    threshold = 50 if data == TEST_CASE else 100

    for coord, distance in distances_to_end.items():
        if distance < threshold:
            # then it's too late to save enough time; bail
            continue
        # All we care about is reachable spaces, not paths
        for dest, cheat_time in generate_coordinates_at_distance(coord):
            time_from_here = distances_to_end.get(dest)
            if time_from_here is None:
                continue
            time_saved = distance - time_from_here - cheat_time
            if time_saved >= threshold:
                cheats[time_saved] += 1

    cheat_count = 0
    for saved, num in sorted(cheats.items()):
        if saved >= threshold:
            if debug:
                print(f'There are {num} cheats that save {saved} picoseconds.')
            cheat_count += num
    return cheat_count


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
        (part_two, {'debug': True}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
