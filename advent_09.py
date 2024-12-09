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
        else:
            empty_space.append((start, n))
        start += n

    checksum = 0
    while files:
        start, size, file_id = files.pop()
        new_location = start
        for i, (space_start, space_size) in enumerate(empty_space):
            if space_size >= size:
                new_location = space_start
                if space_size == size:
                    del empty_space[i]
                else:
                    empty_space[i] = (space_start + size, space_size - size)
                break
        if debug:
            print('>', file_id, new_location)
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
        # (part_one, {'data': DATA}),
        (part_two, {'debug': True}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
