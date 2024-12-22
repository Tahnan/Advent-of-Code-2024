from pathlib import Path

import aoc_util

TEST_CASE = """1
10
100
2024
""".strip()


def parse_data(data):
    return [int(x) for x in data.splitlines()]


def mix(secret, value):
    return secret ^ value


def prune(secret):
    return secret % 16777216


def process(secret):
    secret = prune(mix(secret * 64, secret))
    secret = prune(mix(secret // 32, secret))
    secret = prune(mix(secret * 2048, secret))
    return secret


def part_one(data=TEST_CASE, debug=False):
    buyers = parse_data(data)
    total = 0
    for secret in buyers:
        for _ in range(2000):
            secret = process(secret)
        total += secret
    return total


TEST_CASE_TWO = """1
2
3
2024
""".strip()


def part_two(data=TEST_CASE_TWO, debug=False, truncate=False):
    buyers = parse_data(data)
    buyer_changes = []
    change_history = (None,) * 4
    for secret in buyers:
        buyer_prices = {}
        for _ in range(2000):
            new_secret = process(secret)
            change = (new_secret % 10) - (secret % 10)
            change_history = change_history[1:] + (change,)
            if None not in change_history:
                buyer_prices.setdefault(change_history, new_secret % 10)
            secret = new_secret
        buyer_changes.append(buyer_prices)
    if truncate:
        return buyer_changes
    best = 0
    pattern = None
    for key in set().union(*buyer_changes):
        bananas = sum(bc.get(key, 0) for bc in buyer_changes)
        if bananas > best:
            best = bananas
            pattern = key
    if debug:
        print(pattern)
        print([bc.get(pattern, '-') for bc in buyer_changes])
    return best


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
