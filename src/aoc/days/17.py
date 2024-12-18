from dataclasses import dataclass, field
from enum import IntEnum
from typing import Literal

from aoc.parsers import transform


type Register = Literal["A", "B", "C"]
Registers: list[Register] = ["A", "B", "C"]


class Opcode(IntEnum):
    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bdv = 6
    cdv = 7


@dataclass
class Computer:
    registers: dict[Register, int]
    program: tuple[int, ...]
    _instruction_pointer: int = 0
    _output: list[int] = field(default_factory=list)

    @classmethod
    def from_string(cls, input: str):
        lines = input.split("\n")
        registers = dict[Register, int]()

        for line, register in zip(lines[:3], Registers):
            registers[register] = int(line.split(":")[-1])

        raw_program = lines[-1].split(":")[-1]
        program = tuple(int(x) for x in raw_program.split(","))

        return cls(registers, program)

    def run(self):
        while self._instruction_pointer < len(self.program):
            self._process_instruction()

    def output(self):
        return tuple(self._output)

    def string_output(self):
        return ",".join(str(value) for value in self._output)

    def _process_instruction(self):
        instruction = self.program[self._instruction_pointer]
        operand = self.program[self._instruction_pointer + 1]

        match instruction:
            case Opcode.adv:
                self.registers["A"] //= 2 ** self._combo(operand)
            case Opcode.bxl:
                self.registers["B"] ^= operand
            case Opcode.bst:
                self.registers["B"] = self._combo(operand) % 8
            case Opcode.jnz:
                if self.registers["A"] != 0:
                    self._instruction_pointer = operand
                    # Don't increment instruction pointer further
                    return
            case Opcode.bxc:
                self.registers["B"] ^= self.registers["C"]
            case Opcode.out:
                self._output.append(self._combo(operand) % 8)
            case Opcode.bdv:
                self.registers["B"] = self.registers["A"] // 2 ** self._combo(operand)
            case Opcode.cdv:
                self.registers["C"] = self.registers["A"] // 2 ** self._combo(operand)
            case _:
                raise ValueError(f"Illegal opcode {instruction}")

        self._instruction_pointer += 2

    def _combo(self, operand: int):
        if 0 <= operand <= 3:
            return operand
        if 4 <= operand <= 6:
            register_index = operand - 4
            register = Registers[register_index]
            return self.registers[register]
        raise ValueError(f"Invalid combo operand {operand}")


@transform(Computer.from_string)
def part_1(computer: Computer):
    computer.run()
    return computer.string_output()


def part_2(input: str):
    computer = Computer.from_string(input)

    def run(a: int):
        c = Computer({"A": a}, computer.program)
        c.run()
        return c.output()

    candidates = list[int]()
    prefixes = [0]

    for segment_index in range(4):
        segment_start = -(segment_index + 1) * 4
        program_segment = computer.program[segment_start:]
        print(f"Getting candidates for {program_segment}")

        for prefix in prefixes:
            print(f"Checking prefix {oct(prefix)}")

            for a_suffix in range(0o1000, 0o10000):
                a = prefix + a_suffix
                output = run(a)
                if output == program_segment:
                    print(f"run({oct(a)}) = {output}")
                    candidates.append(a * 4096)
                if output == computer.program:
                    return a

        prefixes = candidates
        candidates = []
