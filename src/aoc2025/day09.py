from itertools import combinations
from pathlib import Path

from .puzzle import AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2025/day/9
"""


class D09Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Initialize attributes
        self._red_tiles: set[tuple[int, int]] = set()

        # Go with input file parsing
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Parse tiles positions
        parsed_line = super().parse_line(index, line)
        x, y = (int(x) for x in parsed_line.split(",", 2))
        self._red_tiles.add((x, y))
        return parsed_line


class D09Step1Puzzle(D09Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        # Find best area from all combinations
        best_area = 0
        for (x1, y1), (x2, y2) in combinations(self._red_tiles, 2):
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if area > best_area:
                best_area = area

        return best_area


class D09Step2Puzzle(D09Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        return 0
