import functools
import operator
import re
from dataclasses import dataclass
from functools import cache
from itertools import combinations, product
from pathlib import Path

from .puzzle import AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2025/day/10
Credit: https://old.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
"""

MACHINE_PATTERN = re.compile("\\[(.+)\\](.+)\\{(.+)\\}")


def patterns(buttons: list[tuple[int, ...]]) -> dict[tuple[int, ...], dict[tuple[int, ...], int]]:
    # Number of buttons and counters
    num_buttons = len(buttons)
    num_counters = len(buttons[0])
    out: dict[tuple[int, ...], dict[tuple[int, ...], int]] = {parity_pattern: {} for parity_pattern in product(range(2), repeat=num_counters)}

    # Iterate on candidate number of button pushes
    for num_pressed_buttons in range(num_buttons + 1):
        # Iterate on combinations
        for buttons_combi in combinations(range(num_buttons), num_pressed_buttons):
            pattern = tuple(map(sum, zip((0,) * num_counters, *(buttons[i] for i in buttons_combi), strict=True)))
            parity_pattern = tuple(i % 2 for i in pattern)
            if pattern not in out[parity_pattern]:
                # Remember number of pushed for this pattern
                out[parity_pattern][pattern] = num_pressed_buttons
    return out


@dataclass
class Machine:
    target: int
    buttons: list[int]
    counter_buttons: list[tuple[int, ...]]
    joltages: tuple[int, ...]

    def buttons_count_to_target(self, target: int) -> int:
        count_candidate = 1
        while True:
            # Iterate on all combinations
            for buttons_combi in combinations(self.buttons, count_candidate):
                # if XOR combination is target, we're good
                if target == functools.reduce(operator.xor, buttons_combi, 0):
                    return count_candidate
            else:
                count_candidate += 1

    def buttons_count_to_joltage(self) -> int:
        pattern_costs = patterns(self.counter_buttons)

        @cache
        def solve_for_pattern(goal: tuple[int, ...]) -> int:
            if all(i == 0 for i in goal):
                return 0
            answer = 1000000
            for pattern, pattern_cost in pattern_costs[tuple(i % 2 for i in goal)].items():
                if all(i <= j for i, j in zip(pattern, goal, strict=True)):
                    new_goal = tuple((j - i) // 2 for i, j in zip(pattern, goal, strict=True))
                    answer = min(answer, pattern_cost + 2 * solve_for_pattern(new_goal))
            return answer

        return solve_for_pattern(self.joltages)


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

            # Parse joltages
            joltages: list[int] = []
            for joltage_str in m.group(3).split(","):
                joltages.append(int(joltage_str))

            # Parse buttons
            buttons: list[int] = []
            counter_buttons: list[tuple[int, ...]] = []
            for button_str in (")" + m.group(2) + "(").split(") ("):
                if button_str:
                    button = 0
                    counter_button: list[int] = [0] * len(joltages)
                    for bit in button_str.split(","):
                        i_bit = int(bit)
                        button += 2 ** int(i_bit)
                        counter_button[i_bit] = 1
                    buttons.append(button)
                    counter_buttons.append(tuple(counter_button))

            # Add machine
            machine = Machine(target, buttons, counter_buttons, tuple(joltages))
            self._logger.info(f"parsed machine on line {index}: {machine}")
            self._machines.append(machine)

        return parsed_line


class D10Step1Puzzle(D10Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        # Iterate on machines
        total = 0
        for machine in self._machines:
            total += machine.buttons_count_to_target(machine.target)

        return total


class D10Step2Puzzle(D10Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        # Iterate on machines
        total = 0
        for machine in self._machines:
            total += machine.buttons_count_to_joltage()

        return total
