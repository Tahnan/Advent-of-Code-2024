from math import inf

from grid_util import Grid, EAST, turn_cw, turn_ccw, move
from pathlib import Path

import aoc_util

TEST_CASE = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
""".strip()


def parse_data(data):
    return Grid.from_text(data)


def part_one(data=TEST_CASE, debug=False):
    grid = parse_data(data)
    start, = {coord for coord, content in grid.items() if content == 'S'}
    end, = {coord for coord, content in grid.items() if content == 'E'}
    direction = EAST
    lowest_cost = {(start, EAST): 0}
    current_options = {(start, EAST): 0}
    best_sol = inf
    while current_options:
        new_options = {}
        for (location, direction), cost in current_options.items():
            # go straight
            forward_state = (move(location, direction), direction)
            move_cost = cost + 1
            if move_cost >= best_sol:
                # ...then turn_cost certainly will be!
                continue
            if grid[forward_state[0]] == '#':
                pass
            elif lowest_cost.get(forward_state, inf) > move_cost:
                lowest_cost[forward_state] = move_cost
                new_options[forward_state] = move_cost
                if forward_state[0] == end:
                    best_sol = move_cost

            # turn CW
            clockwise_state = (location, turn_cw(direction))
            turn_cost = cost + 1000
            if turn_cost >= best_sol:
                continue
            if lowest_cost.get(clockwise_state, inf) > turn_cost:
                lowest_cost[clockwise_state] = turn_cost
                new_options[clockwise_state] = turn_cost

            # turn CCW
            ccw_state = (location, turn_ccw(direction))
            if lowest_cost.get(ccw_state, inf) > turn_cost:
                lowest_cost[ccw_state] = turn_cost
                new_options[ccw_state] = turn_cost
        current_options = new_options
    return best_sol


def part_two(data=TEST_CASE, debug=False):
    grid = parse_data(data)
    start, = {coord for coord, content in grid.items() if content == 'S'}
    end, = {coord for coord, content in grid.items() if content == 'E'}
    direction = EAST
    lowest_cost = {(start, EAST): 0}
    current_options = {(start, EAST): (0, {start})}
    best_sol = inf
    on_a_best_path = set()
    while current_options:
        new_options = {}
        for (location, direction), (cost, path) in current_options.items():
            # go straight
            forward_state = (move(location, direction), direction)
            move_cost = cost + 1
            if move_cost > best_sol:
                # ...then turn_cost certainly will be!
                continue
            if grid[forward_state[0]] == '#':
                pass
            elif lowest_cost.get(forward_state, inf) >= move_cost:
                lowest_cost[forward_state] = move_cost
                new_path = path | {forward_state[0]}
                if forward_state[0] == end:
                    if best_sol > move_cost:
                        best_sol = move_cost
                        on_a_best_path.clear()
                    on_a_best_path.update(new_path)
                else:
                    # this works only as long as getting here with the same
                    # cost takes the same number of moves.  I think?
                    alt_path = new_options.get(forward_state, (None, set()))[1]
                    new_options[forward_state] = (move_cost, new_path | alt_path)

            # turn CW
            clockwise_state = (location, turn_cw(direction))
            turn_cost = cost + 1000
            if turn_cost >= best_sol:
                continue
            if lowest_cost.get(clockwise_state, inf) > turn_cost:
                lowest_cost[clockwise_state] = turn_cost
                alt_path = new_options.get(clockwise_state, (None, set()))[1]
                new_options[clockwise_state] = (turn_cost, path | alt_path)

            # turn CCW
            ccw_state = (location, turn_ccw(direction))
            if lowest_cost.get(ccw_state, inf) > turn_cost:
                lowest_cost[ccw_state] = turn_cost
                alt_path = new_options.get(ccw_state, (None, set()))[1]
                new_options[ccw_state] = (turn_cost, path | alt_path)
        current_options = new_options
    if debug:
        annotated_grid = Grid({**grid})
        annotated_grid.update({coord: 'O' for coord in on_a_best_path})
        print(annotated_grid.to_text())
    return len(on_a_best_path)


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
