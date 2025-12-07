from pathlib import Path

from .puzzle import AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2025/day/7
"""


class D07Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Custom attributes
        self._start_pos = 0
        self._splitters: dict[int, list[int]] = {}

        # Go with input file parsing
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call to get line
        parsed_line = super().parse_line(index, line)

        # Look for start position
        s_pos = parsed_line.find("S")
        if s_pos >= 0:
            self._start_pos = s_pos
            self._logger.info(f"Start position found at index {self._start_pos}")
        else:
            # Locate splitters
            splitters = [i for i, char in enumerate(parsed_line) if char == "^"]
            if splitters:
                self._splitters[index - 1] = splitters
                self._logger.info(f"Splitters found at line {index - 1}: {splitters}")

        return parsed_line


class D07Step1Puzzle(D07Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        # Iterate on splitters to find all beams
        count = 0
        beams: set[int] = set([self._start_pos])
        for y, splitters in self._splitters.items():
            changed = False
            for beam in beams.copy():
                if beam in splitters:
                    beams.remove(beam)
                    beams.add(beam - 1)
                    beams.add(beam + 1)
                    changed = True
                    count += 1
            if changed:
                self._logger.info(f"New beams at line {y}: {sorted(beams)}")

        return count


class D07Step2Puzzle(D07Puzzle):
    def visit_splitter_paths(self, paths_per_start: dict[tuple[int, int], int], start: tuple[int, int]) -> int:
        # Already visited path?
        if start in paths_per_start:
            return paths_per_start[start]

        # Go to next splitter
        x, y = start
        while (y not in self._splitters) or (x not in self._splitters[y]):
            y += 1
            if y >= len(self.input_lines):
                # Reach bottom, only one remaining path
                paths_per_start[start] = 1
                return 1

        # From there, split in two paths
        paths_per_start[start] = self.visit_splitter_paths(paths_per_start, (x - 1, y + 1)) + self.visit_splitter_paths(paths_per_start, (x + 1, y + 1))
        return paths_per_start[start]

    def solve(self, some_arg: int | str | None = None) -> int:
        # Iterate on splitters to find all paths
        return self.visit_splitter_paths({}, (self._start_pos, 0))
