from pathlib import Path

from .puzzle import AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2025/day/5
"""


class D05Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self._ranges: list[tuple[int, int]] = []
        self._ids: list[int] = []
        self._ranges_complete = False
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        parsed_line = super().parse_line(index, line)
        if not parsed_line:
            # Entering second part of the file
            self._ranges_complete = True
        elif not self._ranges_complete:
            # Parse range
            a, b = parsed_line.split("-", 2)
            self._ranges.append((int(a), int(b)))
        else:
            # Parse id
            self._ids.append(int(parsed_line))

        return parsed_line


class D05Step1Puzzle(D05Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        total = 0

        # Iterate on ids
        for some_id in self._ids:
            # Check all ranges
            if any(a <= some_id <= b for a, b in self._ranges):
                total += 1
        return total


class D05Step2Puzzle(D05Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        return 0
