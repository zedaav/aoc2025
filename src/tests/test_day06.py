from aoc2025.day06 import D06Step1Puzzle, D06Step2Puzzle

from .base import AOCPuzzleTester


class TestD06(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D06Step1Puzzle, "d06.sample.txt", 4277556)

    def test_step1_input(self):
        self.check_solution(D06Step1Puzzle, "d06.input.txt", 4648618073226)

    def test_step2_sample(self):
        self.check_solution(D06Step2Puzzle, "d06.sample.txt", 3263827)

    def test_step2_input(self):
        self.check_solution(D06Step2Puzzle, "d06.input.txt", 7329921182115)
