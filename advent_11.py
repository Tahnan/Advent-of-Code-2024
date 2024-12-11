"""
Day 11: Faster than it looks

Part one was clearly "brute force, but this won't work for part two".  Part two
was "wow, brute force doesn't work, what a shock".

What was surprising was thinking, "Why is there so much stress on the linear
nature of the rocks?  Their changes don't depend on neighbors."  Also more
surprising was thinking, "Maybe I can just track the number of each rock, but
probably not, I'll need to keep track of what each X evolves into, and when a
new X appears, I'll..."  But nope, this worked.  Huh.
"""
from collections import defaultdict
from pathlib import Path

import aoc_util

TEST_CASE = """125 17""".strip()


def parse_data(data):
    return [int(x) for x in data.split()]


def part_one(data=TEST_CASE, debug=False):
    # previously: brute force, but it made a handy test case for the revised
    # code
    stones = parse_data(data)
    return _get_stone_count(stones, 25)


def part_two(data=TEST_CASE, debug=False):
    stones = parse_data(data)
    # can we cut it down by just counting the number of each?
    return _get_stone_count(stones, 75)


def _get_stone_count(stones, blinks):
    stone_count = {x: stones.count(x) for x in set(stones)}
    for i in range(blinks):
        new_stone_count = defaultdict(int)
        for stone, num in stone_count.items():
            if stone == 0:
                new_stone_count[1] += num
            elif len(str(stone)) % 2 == 0:
                stone = str(stone)
                half = len(stone) // 2
                new_stone_count[int(stone[:half])] += num
                new_stone_count[int(stone[half:])] += num
            else:
                new_stone_count[2024 * stone] += num
        stone_count = new_stone_count
    return sum(stone_count.values())


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
