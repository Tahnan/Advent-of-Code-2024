from collections import defaultdict
from pathlib import Path

import aoc_util

TEST_CASE = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
""".strip()


def part_one(data=TEST_CASE, debug=False):
    triads = set()
    links = set()
    nodes = set()
    for line in data.strip().splitlines():
        a, b = line.split('-')
        links.update(((a, b), (b, a)))
        for node in nodes:
            if (a, node) in links and (b, node) in links:
                triads.add(tuple(sorted((a, b, node))))
        nodes.update((a, b))
    if debug:
        print('Nodes:', *nodes, sep='\n')
        print('Links:', *links, sep='\n')
        print('Triads:', *triads, sep='\n')
    ts = 0
    for triad in triads:
        if any(x.startswith('t') for x in triad):
            ts += 1
    return ts


class sortedtuple(tuple):
    # At the time, this seemed like a good way to only store a single version
    # of each triad, tetrad, pentad... without having to write "sorted()" in
    # the code every time.
    def __new__(cls, iterable):
        return super().__new__(cls, sorted(iterable))


def part_two(data=TEST_CASE, debug=False):
    # Naming hard.  I don't love "nlans" for lans of size n, but it's better
    # than my first pass where I genericized tri-ad, tetr-ad, ... with n-.
    #
    # Anyway, nlans[1] replaces "nodes", nlans[2] replaces "links', but
    # otherwise it's a lot like part one.
    nlans = defaultdict(set)
    for line in data.strip().splitlines():
        a, b = line.split('-')
        new_nlans = defaultdict(set)
        new_nlans[1] = {sortedtuple((a,)), sortedtuple((b,))}
        new_nlans[2] = {sortedtuple((a, b))}
        level = 3
        # The "insight" here is this: we could add a triad (a, b, c) given
        # the new info a-b if we already knew a-c and b-c.  The same is true of
        # any larger group: since it was just waiting on the a-b connection,
        # a+group and b+group must already be <n>-ads.  Not that this is
        # terribly efficient, but it's got to be nicer than other "try every
        # option" approaches, right?
        while True:
            for group in nlans[level - 2]:
                if (sortedtuple((a, *group)) in nlans[level - 1]
                    and sortedtuple((b, *group)) in nlans[level - 1]):
                    new_nlans[level].add(sortedtuple((a, b, *group)))
            if level not in new_nlans:
                break
            level += 1
        for level, new_things in new_nlans.items():
            nlans[level].update(new_things)
    if debug:
        import pprint
        pprint.pprint(nlans)
    largest_number = max(nlans)
    largest_lan, = nlans[largest_number]
    return ','.join(largest_lan)


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print(time.ctime(), 'Start')
    for fn, kwargs in (
        (part_one, {'debug': True}),
        (part_one, {'data': DATA}),
        (part_two, {'debug': True}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
