from aoc2025.day02 import D02Step1Puzzle, D02Step2Puzzle

from .base import AOCPuzzleTester


class TestD02(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D02Step1Puzzle, "d02.sample.txt", 1227775554)

    def test_step1_input(self):
        self.check_solution(D02Step1Puzzle, "d02.input.txt", 18595663903)

    def test_step2_sample(self):
        self.check_solution(D02Step2Puzzle, "d02.sample.txt", 4174379265)

    def test_step2_input(self):
        self.check_solution(D02Step2Puzzle, "d02.input.txt", 19058204438)
