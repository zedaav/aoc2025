from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .puzzle import AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2025/day/11
"""


@dataclass
class Node:
    name: str
    output_names: set[str]
    all_nodes: dict[str, Node]
    paths_to_out: int | None = None

    def check_output_paths(self) -> int:
        if self.paths_to_out is None:
            self.paths_to_out = 0
            for output_name in self.output_names:
                n = self.all_nodes[output_name]
                self.paths_to_out += n.check_output_paths()
        return self.paths_to_out


class D11Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Initialize attributes
        self._all_nodes: dict[str, Node] = {}
        self._all_nodes["out"] = Node("out", set(), self._all_nodes, 1)

        # Go with input file parsing
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call to get line
        parsed_line = super().parse_line(index, line)
        name, outputs = tuple(parsed_line.split(": ", 2))
        output_names = set(outputs.split(" "))
        self._all_nodes[name] = Node(name, output_names, self._all_nodes)
        return parsed_line


class D11Step1Puzzle(D11Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        # Check all paths to out
        return self._all_nodes["you"].check_output_paths()


class D11Step2Puzzle(D11Puzzle):
    def clear_paths(self):
        for n in self._all_nodes.values():
            n.paths_to_out = None

    def solve(self, some_arg: int | str | None = None) -> int:
        # Check all paths to out
        return self._all_nodes["svr"].check_output_paths()
