"""
Day 17: Scientific progress goes sideways

The first part was easy enough, though honestly I was expecting a longer
program (and have vague memories of self-altering programs; for as short and
non-self-altering as this program is, I could totally have just written it out
procedurally.  In fact, I did that for part two).

And then, oh, part two.  It's not like I expected the brute force approach to
work, particularly, but as noted in a comment below, I didn't have a lot of
enthusiasm for understanding the code.  I ended up understanding it
experimentally rather than analytically: the length of the output was the log
base 8 of the input, the first digit of the input-base-8 affected the last
digit output, etc.

What I ended up running was

powers = [[5]]  # determined by experiment
for exponent in range(15, -1, -1):
    target = program[exponent]
    new_powers = []
    for power in powers:
        for i in range(8):
            repower = power + [i]
            n = sum(p * 8 ** (15 - j) for j, p in enumerate(repower))
            result = run_program(n)
            if result[exponent] == target:
                new_powers.append(repower)
    powers = new_powers

and it failed because something was a float rather than an int (8 ** -1?), and
I was off by one, but whatever, it got me there.
"""
from collections import defaultdict
from math import inf

from grid_util import Grid, EAST, turn_cw, turn_ccw, move
from pathlib import Path

import aoc_util

TEST_CASE = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
""".strip()

TEST_CASE_TWO = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""


def combo_operand(op, registers):
    if 0 <= op <= 3:
        return op
    if op == 4:
        return registers['A']
    if op == 5:
        return registers['B']
    if op == 6:
        return registers['C']
    raise ValueError(f'Unknown op: {op}')


def adv(registers, operand):
    registers['A'] //= (2 ** combo_operand(operand, registers))


def bxl(registers, operand):
    registers['B'] ^= operand


def bst(registers, operand):
    registers['B'] = combo_operand(operand, registers) % 8


def jnz(registers, operand):
    if registers['A'] == 0:
        return
    registers['pointer'] = operand - 2  # so that we can add 2 after


def bxc(registers, operand):
    registers['B'] ^= registers['C']


def out(registers, operand):
    registers['output'].append(combo_operand(operand, registers) % 8)


def bdv(registers, operand):
    registers['B'] = registers['A'] // (2 ** combo_operand(operand, registers))


def cdv(registers, operand):
    registers['C'] = registers['A'] // (2 ** combo_operand(operand, registers))


OPCODES = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv
}


def parse_data(data):
    registers = {'output': [], 'pointer': 0}
    program = None
    for line in data.splitlines():
        if not line:
            continue
        inst, val = line.split(': ')
        if inst.startswith('Register'):
            registers[inst[-1]] = int(val)
        elif inst == 'Program':
            program = [int(v) for v in val.split(',')]
    return registers, program


def part_one(data=TEST_CASE, debug=False):
    registers, program = parse_data(data)
    run_program(registers, program)
    return ','.join(str(n) for n in registers['output'])


def registers_to_states(registers):
    return (registers['A'], registers['B'], registers['C'],
            registers['pointer'])


def run_program(registers, program):
    states = {registers_to_states(registers)}
    while registers['pointer'] < len(program):
        pointer = registers['pointer']
        opcode, operand = program[pointer:pointer + 2]
        OPCODES[opcode](registers, operand)
        registers['pointer'] += 2
        state = registers_to_states(registers)
        if state in states:
            print('ERROR: does not halt')
            return
        states.add(state)


def part_two(data=TEST_CASE, debug=False):
    # This doesn't seem to be a halting problem, which it could have been
    # (maybe? are there programs that don't halt?).  But it does look like the
    # answer is *very* large, which means this requires more introspection,
    # which was always my least favorite part of the "parse this program" days
    # in previous years.
    a = 0
    while True:
        registers, program = parse_data(data)
        registers['A'] = a
        run_program(registers, program)
        if registers['output'] == program:
            return a
        a += 1


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
        (part_two, {'data': TEST_CASE_TWO}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
