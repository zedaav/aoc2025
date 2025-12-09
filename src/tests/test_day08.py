from aoc2025.day08 import D08Step1Puzzle, D08Step2Puzzle

from .base import AOCPuzzleTester


class TestD08(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D08Step1Puzzle, "d08.sample.txt", 40, solve_arg=10)

    def test_step1_input(self):
        self.check_solution(D08Step1Puzzle, "d08.input.txt", 63920, solve_arg=1000)

    def test_step2_sample(self):
        self.check_solution(D08Step2Puzzle, "d08.sample.txt", 25272)

    def test_step2_input(self):
        self.check_solution(D08Step2Puzzle, "d08.input.txt", 1026594680)
