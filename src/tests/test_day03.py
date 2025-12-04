from aoc2025.day03 import D03Step1Puzzle, D03Step2Puzzle

from .base import AOCPuzzleTester


class TestD03(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D03Step1Puzzle, "d03.sample.txt", 357)

    def test_step1_input(self):
        self.check_solution(D03Step1Puzzle, "d03.input.txt", 17087)

    def test_step2_sample(self):
        self.check_solution(D03Step2Puzzle, "d03.sample.txt", 3121910778619)

    def test_step2_input(self):
        self.check_solution(D03Step2Puzzle, "d03.input.txt", 169019504359949)
