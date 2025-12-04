import logging
from pathlib import Path

from .puzzle import OFFSETS, AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2025/day/4
"""


class D04Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self._grid: list[list[str]] = []
        self._width: int = 0
        self._height: int = 0
        super().__init__(input_file)

        # Fill with borders
        self._grid.insert(0, ["."] * (self._width + 2))
        self._grid.append(["."] * (self._width + 2))

    def parse_line(self, index: int, line: str) -> str:
        parsed_line = super().parse_line(index, line)

        # Update width and height
        self._width = len(parsed_line)
        self._height += 1

        # Remember grid line
        self._grid.append(["."] + list(parsed_line) + ["."])

        return parsed_line

    def remove_rolls(self) -> int:
        count = 0
        removed_rolls: set[tuple[int, int]] = set()

        # Iterate on grid cells containing "@"
        for y in range(1, self._height + 1):
            for x in filter(lambda p: self._grid[y][p] == "@", range(1, self._width + 1)):
                # Check neighbors
                filled_neighbor_cells = list(filter(lambda c: c == "@", (self._grid[y + dy][x + dx] for dx, dy in OFFSETS.values())))
                if len(filled_neighbor_cells) < 4:
                    count += 1
                    removed_rolls.add((x, y))

        # Remove rolls
        for x, y in removed_rolls:
            self._grid[y][x] = "."

        logging.debug(f"Removed {count} rolls")
        return count


class D04Step1Puzzle(D04Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        return self.remove_rolls()


class D04Step2Puzzle(D04Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        # Iterate on removing rolls until no more can be removed
        total_removed = 0
        while True:
            removed = self.remove_rolls()
            if removed == 0:
                break
            total_removed += removed
        return total_removed
