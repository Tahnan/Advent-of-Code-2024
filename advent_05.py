"""
Day 5: Let's try something different!  Wait, what was I thinking.

The first part was straightforward enough.  The second part...I feel like the
right thing to do was to take the rules and derive a full ordering, and use
that.  But I thought, what if I had a PageNumber class that could just sort
itself?

I could.  It just took a lot of looking up the details of __lt__ and of sort(),
which ignores the __gt__ that I tried to define.  So it took a while, but good
learning experience, I guess?

ADDENDUM: I realized, walking home, that "a full ordering" is a trap.  The
rules don't guarantee transitivity; "47|53" means that *if both pages are
present*, 47 comes before 53.  But you could have A|B, B|C, C|A, as long as you
never have a set of pages that includes all three.  I don't know if my input
had this case, but it's nice to think I avoided a major pitfall.

POSTSCRIPT: Apparently the input does in fact do this.  Accidental victory!
"""
from collections import defaultdict
from pathlib import Path

import aoc_util

TEST_CASE = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""".strip()


class PageNumber:
    """
    A class that uses a ruleset to define a __lt__ function that can be used
    to sort page numbers.
    """
    def __init__(self, pagenum, ruleset):
        self.pagenum = pagenum
        self.greater_numbers = ruleset[pagenum]
        self.lesser_numbers = set()  # comes after
        for page, afters in ruleset:
            if pagenum in afters:
                self.lesser_numbers.add(page)

    def __lt__(self, other):
        # This number is less than the other number if the other page number
        # is in this number's list of greater numbers, or if this number is
        # in the other's list of lesser numbers
        return (other.pagenum in self.greater_numbers
                or self.pagenum in other.lesser_numbers)

    def __repr__(self):
        return f'<PageNumber: {self.pagenum}>'


def parse_data(data):
    rules, pages = data.split('\n\n')
    ruledict = defaultdict(set)
    for rule in rules.splitlines():
        before, after = rule.split('|')
        ruledict[before].add(after)
    pages = [page.split(',') for page in pages.splitlines()]
    return ruledict, pages


def part_one(data=TEST_CASE, debug=False):
    ruleset, pages = parse_data(data)
    middle_pages = 0
    for page in pages:
        for i, number in enumerate(page):
            must_be_after = ruleset[number]
            if any(mba in page[:i] for mba in must_be_after):
                break
        else:
            # Funny, I was *just saying* how you could use for/else but really
            # it's so counterintuitive that I hate using it.
            middle_pages += int(page[len(page) // 2])
    return middle_pages


def part_two(data=TEST_CASE, debug=False):
    ruleset, pages = parse_data(data)
    middle_pages = 0
    for page in pages:
        paginated = [PageNumber(n, ruleset) for n in page]
        ordered = sorted(paginated)
        if ordered != paginated:
            # probably could have converted to ints in parse_data.  Or put
            # an __int__ on PageNumber.  But, eh.
            middle_pages += int(ordered[len(page) // 2].pagenum)
    return middle_pages


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
