from aoc2025.day01 import D01Step1Puzzle, D01Step2Puzzle

from .base import AOCPuzzleTester


class TestD01(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D01Step1Puzzle, "d01.sample.txt", 3)

    def test_step1_input(self):
        self.check_solution(D01Step1Puzzle, "d01.input.txt", 1078)

    def test_step2_sample(self):
        self.check_solution(D01Step2Puzzle, "d01.sample.txt", 6)

    def test_step2_input(self):
        self.check_solution(D01Step2Puzzle, "d01.input.txt", 6412)
