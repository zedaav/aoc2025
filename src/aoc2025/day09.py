from collections import defaultdict
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
        self._tiles_per_lines: dict[int, set[int]] = defaultdict(set)
        self._first_x = -1
        self._first_y = -1
        self._prev_x = -1
        self._prev_y = -1

        # Go with input file parsing
        super().__init__(input_file)
        self.fill(self._first_x, self._first_y)

    def fill(self, x: int, y: int):
        if (self._prev_x >= 0) and (self._prev_x == x):
            # Fill column
            for other_y in range(min(y, self._prev_y), max(y, self._prev_y)):
                self._tiles_per_lines[other_y].add(x)
        if (self._prev_y >= 0) and (self._prev_y == y):
            # Fill line
            for other_x in range(min(x, self._prev_x), max(x, self._prev_x)):
                self._tiles_per_lines[y].add(other_x)

    def parse_line(self, index: int, line: str) -> str:
        # Parse tiles positions
        parsed_line = super().parse_line(index, line)
        x, y = (int(x) for x in parsed_line.split(",", 2))
        self._red_tiles.add((x, y))
        self._tiles_per_lines[y].add(x)
        self.fill(x, y)
        self._prev_x, self._prev_y = x, y
        if self._first_x < 0 and self._first_y:
            self._first_x, self._first_y = x, y
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
        # Fill all tiles
        all_tiles: set[tuple[int, int]] = set()
        for y in self._tiles_per_lines:
            previous_x = None
            in_row = True
            for x in sorted(self._tiles_per_lines[y]):
                all_tiles.add((x, y))
                if (previous_x is not None) and (x > (previous_x + 1)):
                    # Gap found, fill it?
                    if in_row:
                        # FIXME: this is taking a long time
                        all_tiles.update((ax, y) for ax in range(previous_x, x))
                    in_row = not in_row
                previous_x = x

        # Find best area from all combinations
        best_area = 0
        for (x1, y1), (x2, y2) in combinations(self._red_tiles, 2):
            # Build set with all points
            area = set((x, y) for x in range(min(x1, x2), max(x1, x2) + 1) for y in range(min(y1, y2), max(y1, y2) + 1))
            area_size = len(area)
            # FIXME: this is taking a long time
            if (all_tiles.intersection(area) == area) and (area_size > best_area):
                best_area = area_size
        return best_area
