from aoc2025.day09 import D09Step1Puzzle, D09Step2Puzzle

from .base import AOCPuzzleTester


class TestD09(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D09Step1Puzzle, "d09.sample.txt", 50)

    def test_step1_input(self):
        self.check_solution(D09Step1Puzzle, "d09.input.txt", 4744899849)

    def test_step2_sample(self):
        self.check_solution(D09Step2Puzzle, "d09.sample.txt", 24, solve_arg=(2, 1))  # type: ignore

    def test_step2_input(self):
        self.check_solution(D09Step2Puzzle, "d09.input.txt", 1540192500, solve_arg=(150, 150))  # type: ignore
