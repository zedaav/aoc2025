import re
from dataclasses import dataclass
from pathlib import Path

from .puzzle import AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2025/day/12
"""

# Pattern to parse areas
AREA_PATTERN = re.compile("(\\d+)x(\\d+): ([\\d ]+)")


@dataclass
class Area:
    width: int
    height: int
    requirements: dict[int, int]


class D12Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Initialize attributes
        self._shapes: dict[int, int] = {}
        self._current_shape: int | None = None
        self._areas: list[Area] = []

        # Go with input file parsing
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Get line
        parsed_line = super().parse_line(index, line)

        m = AREA_PATTERN.match(parsed_line)
        if m:
            # Create a new area definition
            width, height = int(m.group(1)), int(m.group(2))
            reqs: dict[int, int] = {}
            for offset, req in enumerate(m.group(3).split(" ")):
                ireq = int(req)
                if ireq:
                    reqs[int(offset)] = ireq
            area = Area(width, height, reqs)
            self._logger.info(f"Parsed area: {area}")
            self._areas.append(area)

        elif not parsed_line:
            # Empty line: reset current shape
            if self._current_shape is not None:
                self._logger.info(f"shape {self._current_shape}: size {self._shapes[self._current_shape]}")
            self._current_shape = None
        elif parsed_line.endswith(":"):
            # Remember current shape id
            self._current_shape = int(re.findall("\\d+", parsed_line)[0])
            self._shapes[self._current_shape] = 0
        elif self._current_shape is not None:
            # New line in current shape
            self._shapes[self._current_shape] += sum(1 if c == "#" else 0 for c in parsed_line)

        return parsed_line


class D12Step1Puzzle(D12Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        total = 0
        for area in self._areas:
            area_size = area.width * area.height
            boxes_size = 0
            for box_id, box_nb in area.requirements.items():
                boxes_size += self._shapes[box_id] * box_nb
            if boxes_size <= area_size:
                total += 1
        return total
