"""
Day 15: auugh more spacial perceptions aaaugh

I wish I had something clever to say here; I shouldn't've waited 24 hours
before putting in commentary.  Mostly I remember that it's once again moving
around on a grid, and (as some of the debugging trail might indicate) I had a
*really* hard time getting my mind around what I needed to have happen.

IIRC, a big part of that was keeping track of "OK, the nearest space is two
steps away.  Wait, does that include where I am?  Does that include the space
I'm moving into?  Do I need to move one crate or two?"  This was true in both
parts.

I *think* get_new_locations could be made general enough to handle both parts
(if it's not already; I didn't think about what it would do with "O", but
possibly it would say "movable obstruction that isn't in '[]'" and do the right
thing with it).  This whole thing needs *so* much more refactoring and
documentation before it's ready to go into robot-controlling production...
"""
from grid_util import Grid, NORTH, SOUTH, EAST, WEST
from pathlib import Path

import aoc_util

TEST_CASE = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""".strip()


SMALL_TEST_CASE = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
""".strip()


DIRS = {'^': NORTH, 'v': SOUTH, '<': WEST, '>': EAST}


def move(start, direction, distance=1):
    x, y = start
    dx, dy = direction
    return (x + dx * distance, y + dy * distance)


def get_steps_to_blank_space_in_dir(start, direction, grid):
    candidate = move(start, direction)
    steps = 0
    while True:
        contents = grid[candidate]
        if contents == '#':
            return
        if contents == '.':
            return steps
        steps += 1
        candidate = move(candidate, direction)


def _gps_coord(coord):
    row, column = coord
    return 100 * row + column


def parse_data(data):
    grid, moves = data.split('\n\n')
    grid = Grid.from_text(grid)
    moves = moves.replace('\n', '')
    return grid, moves


def part_one(data=TEST_CASE, debug=False):
    grid, moves = parse_data(data)
    robot, = [coord for coord, content in grid.items() if content == '@']
    for step in moves:
        direction = DIRS[step]
        distance = get_steps_to_blank_space_in_dir(robot, direction, grid)
        if distance is None:
            if debug:
                print(f'Move {step}:')
                print('No change.')
                print()
            continue
        grid[robot] = '.'
        new_robot = move(robot, direction)
        grid[new_robot] = '@'
        for dist in range(2, distance + 2):
            grid[move(robot, direction, distance=dist)] = 'O'
        robot = new_robot
        if debug:
            print(f'Move {step}:')
            print(grid.to_text())
            print()
    gps_sum = 0
    for coord, contents in grid.items():
        if contents == 'O':
            gps_sum += _gps_coord(coord)
    return gps_sum


def _get_new_locations(start, direction, grid):
    # like move(), but worse
    next_space = move(start, direction)
    new_locations = {start: '.', next_space: '@'}
    contents = grid[next_space]
    if contents == '#':
        return {}
    if contents == '.':
        return new_locations
    if direction in (EAST, WEST):
        # Moving horizontally is much like before!
        steps = get_steps_to_blank_space_in_dir(start, direction, grid)
        if steps is None:
            return {}
        for dist in range(1, steps + 1):
            move_from = move(start, direction, distance=dist)
            move_to = move(start, direction, distance=dist + 1)
            new_locations[move_to] = grid[move_from]
        return new_locations
    # If we made it here, it means we have a N/S move into a box. Yay.
    moving_from = {start}
    while True:
        moving_to = set()
        for move_from in moving_from:
            move_to = move(move_from, direction)
            contents = grid[move_to]
            if contents == '#':
                return {}
            new_locations[move_to] = grid[move_from]
            if contents in '[]':
                moving_to.add(move_to)
                partner_dir = EAST if contents == '[' else WEST
                if move(move_from, partner_dir) not in moving_from:
                    partner = move(move_to, partner_dir)
                    moving_to.add(partner)
                    new_locations[partner] = '.'
        if not moving_to:
            return new_locations
        moving_from = moving_to


def part_two(data=TEST_CASE, debug=False):
    data = (data.replace('#', '##')
                .replace('O', '[]')
                .replace('.', '..')
                .replace('@', '@.'))
    grid, moves = parse_data(data)
    robot, = [coord for coord, content in grid.items() if content == '@']
    for i, step in enumerate(moves):
        direction = DIRS[step]
        new_spaces = _get_new_locations(robot, direction, grid)
        if new_spaces:
            robot = move(robot, direction)
            grid.update(new_spaces)
        if debug and 20 <= i <= 21:
            print(f'{i}. Move {step}:')
            print(grid.to_text())
            print()
    gps_sum = 0
    for coord, contents in grid.items():
        if contents == '[':
            gps_sum += _gps_coord(coord)
    return gps_sum


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print(time.ctime(), 'Start')
    for fn, kwargs in (
        # (part_one, {'data': SMALL_TEST_CASE, 'debug': True}),
        (part_one, {}),
        (part_one, {'data': DATA}),
        (part_two, {'debug': True}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
