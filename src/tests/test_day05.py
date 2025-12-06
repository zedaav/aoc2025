from aoc2025.day05 import D05Step1Puzzle, D05Step2Puzzle

from .base import AOCPuzzleTester


class TestD05(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D05Step1Puzzle, "d05.sample.txt", 3)

    def test_step1_input(self):
        self.check_solution(D05Step1Puzzle, "d05.input.txt", 848)

    def test_step2_sample(self):
        self.check_solution(D05Step2Puzzle, "d05.sample.txt", 14)

    def test_step2_input(self):
        self.check_solution(D05Step2Puzzle, "d05.input.txt", 334714395325710)
