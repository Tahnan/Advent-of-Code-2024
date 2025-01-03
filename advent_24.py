from collections import defaultdict
from pathlib import Path

import aoc_util

TEST_CASE = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
""".strip()


class Gate:
    def __init__(self, op, out):
        self.vals = []
        self.op = op
        self.out = out

    def add_input(self, value):
        self.vals.append(value)
        if len(self.vals) == 2:
            return self.trigger()

    def trigger(self):
        a, b = self.vals
        if self.op == 'AND':
            value = a & b
        elif self.op == 'OR':
            value = a | b
        elif self.op == 'XOR':
            value = a ^ b
        else:
            raise RuntimeError(f"I'm a {self.op} gate!")
        return self.out, value


class GateOverseer:
    def __init__(self):
        self.input_to_gates = defaultdict(list)

    def add_gate(self, gateline):
        in1, op, in2, _, out = gateline.split()
        gate = Gate(op, out)
        self.input_to_gates[in1].append(gate)
        self.input_to_gates[in2].append(gate)

    def send_input_to_gates(self, wire, value):
        for gate in self.input_to_gates[wire]:
            response = gate.add_input(value)
            if response is not None:
                yield response


class SystemOverseer:
    def __init__(self, data):
        self.wires_to_values_to_send = []
        self.gate_overseer = GateOverseer()
        wires, gates = data.split('\n\n')
        for gate in gates.splitlines():
            self.gate_overseer.add_gate(gate)
        for line in wires.splitlines():
            wire, value = line.split(': ')
            self.wires_to_values_to_send.append((wire, int(value)))

    def trigger(self):
        z_wires = []
        while self.wires_to_values_to_send:
            wire, value = self.wires_to_values_to_send.pop()
            if wire.startswith('z'):
                z_wires.append((wire, value))
            self.wires_to_values_to_send.extend(
                self.gate_overseer.send_input_to_gates(wire, value)
            )
        z_wires.sort(reverse=True)
        return int(''.join(str(val) for wire, val in z_wires), 2)


def part_one(data=TEST_CASE, debug=False):
    overseer = SystemOverseer(data)
    return overseer.trigger()


def part_two(data=TEST_CASE, debug=False):
    pass


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
