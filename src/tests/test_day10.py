from aoc2025.day10 import D10Step1Puzzle, D10Step2Puzzle

from .base import AOCPuzzleTester


class TestD10(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D10Step1Puzzle, "d10.sample.txt", 7)

    def test_step1_input(self):
        self.check_solution(D10Step1Puzzle, "d10.input.txt", 409)

    def test_step2_sample(self):
        self.check_solution(D10Step2Puzzle, "d10.sample.txt", 33)

    def test_step2_input(self):
        self.check_solution(D10Step2Puzzle, "d10.input.txt", 15489)
