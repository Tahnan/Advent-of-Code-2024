"""
Day 19: I think I got the "naming things" part OK?

Part one was surprisingly easy with regular expressions.  (four minutes, 301st
place levels of easy.)  But I was going to have way more problems if I tried to
use them in part two.  (Wow, today is all about the CS memes, huh?)

So I wrote the recursive algorithm for part two and ran it.  It was clearly
going to take forever.  I added the PATTERN_RE check to weed out impossible
cases, but that, too, was going to take forever.  So I put in a cache to keep
track of known states, since I figured that in a lot of cases it was "there are
two ways to do the first three stripes, and then we're re-calculating all the
ways to do the remaining 82" or whatever.  Boom!  Much faster.

Also wrong.

But the test worked, so it was hard to debug.  I poked.  And poked some more.
And then I realized the problem was...I had set up a global cache.  And I hadn't
cleared it after running the test.

Yeah.
"""
import re
from pathlib import Path

import aoc_util
from grid_util import CARDINALS, DIRECTIONS, move

TEST_CASE = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
""".strip()

RE_PATTERN = None
PATTERN_CACHE = {}


def parse_data(data):
    available, desired = data.split('\n\n')
    return available.split(', '), desired.splitlines()


def part_one(data=TEST_CASE, debug=False):
    available, desired = parse_data(data)
    pattern = re.compile('(' + '|'.join(available) + ')*')
    possible = 0
    for design in desired:
        if pattern.fullmatch(design):
            possible += 1
    return possible


def possibilities(pattern, available, depth=0, debug=False):
    if pattern in PATTERN_CACHE:
        return PATTERN_CACHE[pattern]
    if not RE_PATTERN.fullmatch(pattern):
        return 0
    if not pattern:
        # unreachable I think?
        return 0
    score = 0
    available = {x for x in available if x in pattern}
    if debug:
        print('>' * (depth + 2), len(available))
    for avail in available:
        if pattern == avail:
            score += 1
        elif pattern.startswith(avail):
            score += possibilities(pattern[len(avail):], available,
                                   depth=depth + 1, debug=debug)
    PATTERN_CACHE[pattern] = score
    return score


# 884345336835163 is wrong
def part_two(data=TEST_CASE, debug=False):
    global RE_PATTERN, PATTERN_CACHE
    available, desired = parse_data(data)
    RE_PATTERN = re.compile('(' + '|'.join(available) + ')*')
    PATTERN_CACHE.clear()
    possible = 0
    for desire in desired:
        this_possible = possibilities(desire, available)
        possible += this_possible
        if debug:
            print('>', desire, this_possible)
    return possible


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
