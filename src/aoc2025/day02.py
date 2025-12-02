import logging
from functools import cache
from pathlib import Path

from .puzzle import AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2025/day/2
"""


@cache
def patterns_for_len(length: int) -> list[int]:
    # Find all patterns for given length
    patterns: list[int] = []
    for pattern_len in range(1, length):
        if length % pattern_len == 0:
            patterns.append(int(f"{1:0{pattern_len}d}" * (length // pattern_len)))
    logging.info(f"Patterns for length {length}: {patterns}")
    return patterns


class D02Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.ranges: list[tuple[int, int]] = []
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call to get line
        main_line = super().parse_line(index, line)

        # Iterate on ranges
        for range in main_line.split(","):
            start, end = range.split("-", 1)
            self.ranges.append((int(start), int(end)))

        return main_line


class D02Step1Puzzle(D02Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        invalid_ids_sum = 0

        # Iterate on ranges
        for start, end in self.ranges:
            # Iterate on candidates
            for candidate_id in range(start, end + 1):
                candidate_id_str = str(candidate_id)
                candidate_len = len(candidate_id_str)
                if (candidate_len % 2 == 0) and (candidate_id_str[: candidate_len // 2] == candidate_id_str[candidate_len // 2 :]):
                    # Both halves are equal -> invalid
                    logging.debug(f"Invalid ID found in range {start}-{end}: {candidate_id}")
                    invalid_ids_sum += candidate_id

        return invalid_ids_sum


class D02Step2Puzzle(D02Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        invalid_ids_sum = 0

        # Iterate on ranges
        for start, end in self.ranges:
            # Iterate on candidates
            found_range_candidates: set[int] = set()
            for candidate_id in range(start, end + 1):
                candidate_id_str = str(candidate_id)
                candidate_len = len(candidate_id_str)
                # Iterate on patterns
                for pattern in patterns_for_len(candidate_len):
                    if (candidate_id not in found_range_candidates) and (candidate_id % pattern) == 0:
                        # Divisible by pattern -> invalid
                        logging.debug(f"Invalid ID found in range {start}-{end}: {candidate_id}")
                        found_range_candidates.add(candidate_id)
                        invalid_ids_sum += candidate_id

        return invalid_ids_sum
