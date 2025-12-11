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

    def check_output_paths(self, excluded_nodes: set[str] | None = None) -> int:
        if self.paths_to_out is None:
            self.paths_to_out = 0
            for output_name in filter(lambda nd: excluded_nodes is None or nd not in excluded_nodes, self.output_names):
                n = self.all_nodes[output_name]
                self.paths_to_out += n.check_output_paths(excluded_nodes)
        return self.paths_to_out


class D11Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Initialize attributes
        self._all_nodes: dict[str, Node] = {}
        self._all_nodes["out"] = Node("out", set(), self._all_nodes)

        # Go with input file parsing
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call to get line
        parsed_line = super().parse_line(index, line)
        name, outputs = tuple(parsed_line.split(": ", 2))
        output_names = set(outputs.split(" "))
        self._all_nodes[name] = Node(name, output_names, self._all_nodes)
        return parsed_line

    def paths_to_target(self, start: str, target: str, excluded_nodes: set[str] | None = None) -> int:
        # Clear all paths first
        for n in self._all_nodes.values():
            n.paths_to_out = None

        # Target path set to 1
        self._all_nodes[target].paths_to_out = 1

        # Check all paths
        return self._all_nodes[start].check_output_paths(excluded_nodes)


class D11Step1Puzzle(D11Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        # Check all paths from you to out
        return self.paths_to_target("you", "out")


class D11Step2Puzzle(D11Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        # Count paths:
        svr2dac = self.paths_to_target("svr", "dac", {"fft", "out"})  # svr --> dac
        svr2fft = self.paths_to_target("svr", "fft", {"dac", "out"})  # svr --> fft
        dac2fft = self.paths_to_target("dac", "fft", {"svr", "out"})  # dac --> fft
        fft2dac = self.paths_to_target("fft", "dac", {"svr", "out"})  # fft --> dac
        dac2out = self.paths_to_target("dac", "out", {"svr", "fft"})  # dac --> out
        fft2out = self.paths_to_target("fft", "out", {"svr", "dac"})  # fft --> out

        # Check all paths to out
        return svr2dac * dac2fft * fft2out + svr2fft * fft2dac * dac2out
