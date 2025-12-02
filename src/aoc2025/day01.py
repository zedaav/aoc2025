from pathlib import Path

from .puzzle import AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2025/day/1
"""


class D01Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self._offsets: list[int] = []
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Parse offset
        input_line = super().parse_line(index, line)
        self._offsets.append(int(input_line[1:]) * (-1 if input_line[0] == "L" else 1))
        return input_line


class D01Step1Puzzle(D01Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        # Start from 50 and update
        pos = 50
        zeroes = 0
        for offset in self._offsets:
            pos = (pos + (offset % 100)) % 100
            if pos == 0:
                zeroes += 1

        return zeroes


class D01Step2Puzzle(D01Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        # Start from 50 and update
        pos = 50
        zeroes = 0
        for offset in self._offsets:
            # Additionally count overlapping zeroes
            zeroes += abs(offset) // 100

            # Position candidate
            offset_sign = 1 if (offset > 0) else -1
            pos_candidate = pos + (offset % (100 * offset_sign)) + 100

            # Maybe an additional zero?
            if (pos != 0) and ((pos_candidate < 100) or (pos_candidate > 200)):
                zeroes += 1

            # Final position
            pos = pos_candidate % 100
            if pos == 0:
                zeroes += 1

        return zeroes
