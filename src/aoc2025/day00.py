from pathlib import Path

from .puzzle import AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2025/day/0
"""


class D00Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # TODO: Initialize attributes here

        # Go with input file parsing
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call to get line
        parsed_line = super().parse_line(index, line)
        self._logger.info(f">>> parsed line: {parsed_line}")
        return parsed_line


class D00Step1Puzzle(D00Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        return 0


class D00Step2Puzzle(D00Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        return 0
