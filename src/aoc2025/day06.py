import logging
import re
from collections.abc import Generator
from pathlib import Path
from typing import Any, cast

import numpy as np
from numpy._typing import NDArray

from .puzzle import AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2025/day/6
"""


class D06Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self._input_letters: NDArray[Any] | None = None
        self._operators: list[str] = []
        self._nrows, self._ncols = 0, 0
        super().__init__(input_file)
        logging.debug(f"Input letters ({self._nrows}x{self._ncols}):\n{self._input_letters}")

        # Find separators in rows
        assert self._input_letters is not None
        _sep_col_mask = np.all(self._input_letters == " ", axis=0)
        logging.debug(f"Separator column mask:\n{_sep_col_mask}")
        ranges: list[tuple[int, int]] = []
        previous_index = 0
        for _sep_col_index in np.where(_sep_col_mask)[0]:
            ranges.append((int(previous_index), int(_sep_col_index) - 1))
            previous_index = _sep_col_index + 1
        ranges.append((int(previous_index), int(self._ncols) - 1))
        logging.debug(f"Block ranges:\n{ranges}")

        # Build blocks
        self._input_blocks: list[NDArray[Any]] = []
        for start_col, end_col in ranges:
            block = self._input_letters[:, start_col : end_col + 1]
            self._input_blocks.append(block)
        logging.debug(f"Input blocks: {len(self._input_blocks)}")

        # Build input numbers
        self._input_numbers = self._parse_numbers_from_blocks()

    def parse_line(self, index: int, line: str) -> str:
        parsed_line = line.strip("\r\n")
        if parsed_line[0] in ["*", "+"]:
            # Remember operators
            self._operators = [op for op in re.findall(r"[\*\+]", parsed_line)]
            logging.debug(f"Operators: {self._operators}")
        else:
            # Add line
            row_list = [list(parsed_line)]
            if self._input_letters is None:
                self._input_letters = np.array(row_list)
            else:
                self._input_letters = np.append(self._input_letters, row_list, axis=0)

            # Update sizes
            self._nrows, self._ncols = self._input_letters.shape
        return parsed_line

    def _parse_numbers_from_blocks(self) -> list[NDArray[Any]]:
        # Iterate on blocks
        output: list[NDArray[Any]] = []
        for block in self.consume_blocks():
            numbers = np.array([int("".join(row)) for row in block])
            output.append(numbers)
        logging.debug(f"Input numbers:\n{output}")
        return output

    def consume_blocks(self) -> Generator[NDArray[Any], None, None]:
        yield from self._input_blocks

    def solve(self, some_arg: int | str | None = None) -> int:
        # Iterate on rows
        total: int = 0
        for row, operator in zip(self._input_numbers, self._operators, strict=True):
            if operator == "*":
                # Product
                total += cast(int, np.prod(row))
            elif operator == "+":
                # Sum
                total += cast(int, np.sum(row))
        return total


class D06Step1Puzzle(D06Puzzle):
    pass


class D06Step2Puzzle(D06Puzzle):
    def consume_blocks(self) -> Generator[NDArray[Any], None, None]:
        for block in self._input_blocks:
            yield block.T
