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
    def largest_subnumber(number: list[int], k: int) -> int:
        n = len(number)
        stack: list[int] = []
        to_remove = n - k  # How many we are allowed to drop overall
        for x in number:
            # While we can remove something and last < x, pop to allow a larger digit earlier
            while stack and to_remove > 0 and stack[-1] < x:
                stack.pop()
                to_remove -= 1
            stack.append(x)

        # If we didn't remove enough, trim the end
        stack = stack[:k]

        result = 0
        for pos, d in enumerate(stack[::-1]):
            result += d * (10**pos)
        return result


class D03Step1Puzzle(D03Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        result = 0
        for battery in self._batteries:
            result += self.largest_subnumber(battery, 2)
        return result


class D03Step2Puzzle(D03Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        result = 0
        for battery in self._batteries:
            result += self.largest_subnumber(battery, 12)
        return result
