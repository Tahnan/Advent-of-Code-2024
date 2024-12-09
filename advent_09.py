"""
Day 9: Finally, something I can screw up *subtly*!

I did part one with brute force, even though I knew that was a bad idea (and it
takes eleven seconds to run).  Part two was clearly going to need something
more clever.

I am kind of proud that I pretty quickly hit on the fact that once you'd
evaluated a file_id, you knew its final location and could go ahead and add it
to the checksum immediately, rather than holding onto the information *and*
iterating over a very long list at the end.  I got a false start by trying to
track the empty space by size, forgetting that something of size 2 would slot
into (part of) a size-three space that cames before an exact-fit size-two space.
But that didn't take long to fix, and I realized that part before running.

If you compare this commit to the previous one, though, you'll see that I missed
a crucial fact: things only move *earlier*, and I needed to stop looking for
space once I hit the location of the file_id.  (Which ironically also makes it
faster.)  This didn't come up in the test case, and it took some scrutinizing
my debug information to get there.

But, hey, I got there.  Tempted to rewrite the first part to look more like the
second, to see if I can get it to run faster, but it might not be worth it.
"""
from pathlib import Path

import aoc_util

TEST_CASE = """
2333133121414131402
""".strip()


def parse_data(data):
    disk = []
    for i, n in enumerate(data.strip()):
        if i % 2 == 0:
            disk.extend([i // 2] * int(n))
        else:
            disk.extend([None] * int(n))
    return disk


def part_one(data=TEST_CASE, debug=False):
    disk = parse_data(data)
    while None in disk:
        end = disk.pop()
        if end is not None:
            disk[disk.index(None)] = end
    checksum = 0
    for i, n in enumerate(disk):
        checksum += i * n
    return checksum


def part_two(data=TEST_CASE, debug=False):
    # Yeah, brute force wasn't gonna work for this.
    # New parse_data:
    files = []
    empty_space = []
    start = 0
    for i, n in enumerate(data.strip()):
        n = int(n)
        if i % 2 == 0:
            files.append((start, n, i // 2))
        elif n:
            empty_space.append((start, n))
        start += n

    checksum = 0
    while files:
        start, size, file_id = files.pop()
        new_location = start
        for i, (space_start, space_size) in enumerate(empty_space):
            if space_start > start:
                break
            if space_size >= size:
                new_location = space_start
                if space_size == size:
                    del empty_space[i]
                else:
                    empty_space[i] = (space_start + size, space_size - size)
                break
        if debug:
            print('>', file_id, new_location)
            print('>>', empty_space)
        for loc in range(new_location, new_location + size):
            checksum += loc * file_id
    return checksum


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
    print('IS NOT 8593662006385')
