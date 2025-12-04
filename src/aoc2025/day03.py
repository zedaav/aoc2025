from pathlib import Path

from .puzzle import AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2025/day/3
"""


class D03Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self._batteries: list[list[int]] = []
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call to get line
        parsed_line = super().parse_line(index, line)
        self._batteries.append([int(i) for i in parsed_line])
        return parsed_line

    @staticmethod
    def find_max(cells: list[int]) -> tuple[int, int]:
        candidate_max = 0
        candidate_pos = 0
        for pos, i in enumerate(cells):
            if i > candidate_max:
                candidate_max = i
                candidate_pos = pos
                if candidate_max == 9:
                    break
        return (candidate_pos, candidate_max)


class D03Step1Puzzle(D03Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        result = 0
        for battery in self._batteries:
            # First max
            pos1, max1 = self.find_max(battery)

            # Secondary maximums
            if pos1 > 0:
                _, max0 = self.find_max(battery[0:pos1])
            else:
                _, max0 = None, None
            if pos1 < len(battery) - 1:
                _, max2 = self.find_max(battery[pos1 + 1 :])
            else:
                _, max2 = None, None

            # Prepare candidate
            candidates: list[int] = []
            if max0:
                candidates.append(max0 * 10 + max1)
            if max2:
                candidates.append(max1 * 10 + max2)

            # Use the max of them
            joltage = max(candidates)
            result += joltage
        return result


class D03Step2Puzzle(D03Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        return 0
