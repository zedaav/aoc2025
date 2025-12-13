from aoc2025.day12 import D12Step1Puzzle

from .base import AOCPuzzleTester


class TestD12(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D12Step1Puzzle, "d12.sample.txt", 3)

    def test_step1_input(self):
        self.check_solution(D12Step1Puzzle, "d12.input.txt", 440)
