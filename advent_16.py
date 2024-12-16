from collections import defaultdict
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
    lowest_cost = defaultdict(lambda: (inf, set()))
    lowest_cost[(start, EAST)] = (0, {start})
    current_options = {(start, EAST)}
    best_sol = inf
    while current_options:
        new_options = set()
        for (location, direction) in current_options:
            cost, path = lowest_cost[(location, direction)]

            # go straight
            forward_state = (move(location, direction), direction)
            move_cost = cost + 1
            if move_cost > best_sol:
                # ...then turn_cost certainly will be!
                continue
            if grid[forward_state[0]] == '#':
                pass
            elif forward_state[0] == end and move_cost > best_sol:
                pass
            else:
                prev_cost, prev_path = lowest_cost[forward_state]
                if move_cost <= prev_cost:
                    new_path = path | {forward_state[0]}
                    if move_cost == prev_cost:
                        new_path |= prev_path
                    lowest_cost[forward_state] = (move_cost, new_path)

                    if forward_state[0] == end:
                        best_sol = move_cost
                    else:
                        new_options.add(forward_state)

            turn_cost = cost + 1000
            # turn CW
            clockwise_state = (location, turn_cw(direction))
            if turn_cost >= best_sol:
                continue
            prev_cost, prev_path = lowest_cost[clockwise_state]
            if turn_cost <= prev_cost:
                new_path = path
                if move_cost == prev_cost:
                    new_path |= prev_path
                lowest_cost[clockwise_state] = (turn_cost, new_path)
                new_options.add(clockwise_state)

            # turn CCW
            ccw_state = (location, turn_ccw(direction))
            prev_cost, prev_path = lowest_cost[ccw_state]
            if turn_cost <= prev_cost:
                new_path = path
                if move_cost == prev_cost:
                    new_path |= prev_path
                lowest_cost[ccw_state] = (turn_cost, new_path)
                new_options.add(ccw_state)
        current_options = new_options
    on_a_best_path = set()
    for (coord, _), (cost, path) in lowest_cost.items():
        if coord == end:
            on_a_best_path.update(path)
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
