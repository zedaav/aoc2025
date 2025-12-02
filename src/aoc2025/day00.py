import logging

from .puzzle import AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2025/day/0
"""


class D00Puzzle(AOCPuzzle):
    def parse_line(self, index: int, line: str) -> str:
        # Super call to get line
        logging.info(">>> parsed line")
        return super().parse_line(index, line)


class D00Step1Puzzle(D00Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        return 0


class D00Step2Puzzle(D00Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        return 0
