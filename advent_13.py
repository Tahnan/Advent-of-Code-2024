"""
Day 13: Mad and unimpressed

So this was...algebra?  Not even hard algebra, more like "first month of high
school algebra".  I wasn't particularly fooled by the weird phrasing of "the
cheapest way to win the prize" -- you have two equations with two variables, it
has exactly one solution (that might or might not be integers) -- but I was
kind of irritated by it.  Why is it being phrased as if there are multiple
solutions for each machine?  Is he just trying to trick people into using
some brute force "try every combination of a = [0, 100], b = [0, 100]"?

I was also annoyed that I tried to dredge up, and then websearch, enough linear
algebra to do it by matrices (without bothering to install numpy, which always
feels like overkill) rather than just doing the algebra and being done with it.

Ultimately, it was a boring problem that still took me too damned long to do.
"""
from pathlib import Path

import aoc_util

TEST_CASE = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
""".strip()


def parse_data(data):
    machines = data.split('\n\n')
    parsed = []
    for machine in machines:
        a, b, prize = machine.splitlines()
        a = [int(x.strip('XY+,')) for x in a.split()[-2:]]
        b = [int(x.strip('XY+,')) for x in b.split()[-2:]]
        prize = [int(x.strip('XY=,')) for x in prize.split()[-2:]]
        parsed.append((a, b, prize))
    return parsed


def _solve_machine(machine):
    # Basic algebra:
    #  (M, N), (X, Y), (P, Q) -->
    #  aM + bX = P ... aMY + bXY = PY
    #  aN + bY = Q ... aNX + bYX = QX
    #  a(MY - NX) = (PY - QX) ... a = (PY - QX) / (MY - NX)
    (ax, ay), (bx, by), (px, py) = machine
    a = (px * by - py * bx) / (ax * by - ay * bx)
    b = (px - ax * a) / bx
    return a, b


def part_one(data=TEST_CASE, debug=False):
    machines = parse_data(data)
    cost = 0
    for machine in machines:
        try:
            a, b = _solve_machine(machine)
        except ZeroDivisionError:
            continue
        if int(a) == a and int(b) == b:
            cost += 3 * a + b
    return cost


def part_two(data=TEST_CASE, debug=False):
    offset = 10000000000000
    machines = parse_data(data)
    machines = [(x, y, (p1 + offset, p2 + offset))
                for x, y, (p1, p2) in machines]
    cost = 0
    for machine in machines:
        try:
            a, b = _solve_machine(machine)
        except ZeroDivisionError:
            continue
        if int(a) == a and int(b) == b:
            cost += 3 * a + b
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
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
