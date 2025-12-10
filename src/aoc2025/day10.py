import functools
import operator
import re
from dataclasses import dataclass
from itertools import combinations, combinations_with_replacement
from pathlib import Path

from .puzzle import AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2025/day/10
"""

MACHINE_PATTERN = re.compile("\\[(.+)\\](.+)\\{(.+)\\}")


@dataclass
class Machine:
    target: int
    buttons: set[int]
    counter_buttons: list[list[int]]
    joltages: list[int]


class D10Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Initialize attributes
        self._machines: list[Machine] = []

        # Go with input file parsing
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Parse line
        parsed_line = super().parse_line(index, line)
        m = MACHINE_PATTERN.match(parsed_line)
        if m:
            # Parse target
            target = 0
            for i, c in enumerate(m.group(1)):
                if c == "#":
                    target += 2**i

            # Parse buttons
            buttons: set[int] = set()
            counter_buttons: list[list[int]] = []
            for button_str in (")" + m.group(2) + "(").split(") ("):
                if button_str:
                    button = 0
                    counter_button: list[int] = []
                    for bit in button_str.split(","):
                        button += 2 ** int(bit)
                        counter_button.append(int(bit))
                    buttons.add(button)
                    counter_buttons.append(counter_button)

            # Parse joltages
            joltages: list[int] = []
            for joltage_str in m.group(3).split(","):
                joltages.append(int(joltage_str))

            # Add machine
            machine = Machine(target, buttons, counter_buttons, joltages)
            self._logger.info(f"parsed machine on line {index}: {machine}")
            self._machines.append(machine)

        return parsed_line


class D10Step1Puzzle(D10Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        # Iterate on machines
        total = 0
        for machine in self._machines:
            count_candidate = 1
            found_candidate = 0
            while found_candidate == 0:
                # Iterate on all combinations
                for buttons_combi in combinations(machine.buttons, count_candidate):
                    # if XOR combination is target, we're good
                    if machine.target == functools.reduce(operator.xor, buttons_combi, 0):
                        found_candidate = count_candidate
                        break
                else:
                    count_candidate += 1
            total += found_candidate

        return total


class D10Step2Puzzle(D10Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        # Iterate on machines
        total = 0
        for machine in self._machines:
            count_candidate = 1
            found_candidate = 0
            while found_candidate == 0:
                # Iterate on all combinations
                for buttons_combi in combinations_with_replacement(machine.counter_buttons, count_candidate):
                    # Compute counters from button pushes
                    counters = [0] * len(machine.joltages)
                    for button in buttons_combi:
                        for pos in button:
                            counters[pos] = counters[pos] + 1
                    # If counters match joltages, we're good
                    if counters == machine.joltages:
                        found_candidate = count_candidate
                        break
                else:
                    count_candidate += 1
            total += found_candidate
        return total
