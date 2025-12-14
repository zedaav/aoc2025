from collections import deque
from collections.abc import Iterable
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt

from .puzzle import CARDINAL_DIRS, OFFSETS, AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2025/day/9
"""


def compress_coordinates(corners: list[tuple[int, int]]) -> list[tuple[int, int]]:
    x_values = [c[0] for c in corners]
    y_values = [c[1] for c in corners]
    unique_x, unique_y = sorted(set(x_values)), sorted(set(y_values))
    x_rank = {x: i for i, x in enumerate(unique_x)}
    y_rank = {y: i for i, y in enumerate(unique_y)}
    return [(x_rank[x], y_rank[y]) for x, y in corners]


def plot_points(points: Iterable[tuple[int, int]], point_size: int = 2):
    xs, ys = zip(*points, strict=True)
    plt.figure(figsize=(10, 10))  # type: ignore
    plt.scatter(xs, ys, s=point_size)  # type: ignore
    plt.xlabel("X")  # type: ignore
    plt.ylabel("Y")  # type: ignore
    plt.grid(True)  # type: ignore
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()  # type: ignore


def span(c1: tuple[int, int], c2: tuple[int, int]):
    x1, y1 = c1
    x2, y2 = c2
    x_min, x_max = sorted((x1, x2))
    y_min, y_max = sorted((y1, y2))
    return {(x, y) for x in range(x_min, x_max + 1) for y in range(y_min, y_max + 1)}


def create_borders(coordinates: list[tuple[int, int]]) -> set[tuple[int, int]]:
    borders: set[tuple[int, int]] = set()
    complete = coordinates + [coordinates[0]]
    for c1, c2 in zip(complete, complete[1:], strict=False):
        borders |= span(c1, c2)
    return borders


class D09Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Initialize attributes
        self._corners: list[tuple[int, int]] = []

        # Go with input file parsing
        super().__init__(input_file)

        # Compress coordinates
        self._compressed = compress_coordinates(self._corners)
        # plot_points(self._compressed)

        # Compute border
        self._borders = create_borders(self._compressed)

    def parse_line(self, index: int, line: str) -> str:
        # Parse tiles positions
        parsed_line = super().parse_line(index, line)
        x, y = (int(x) for x in parsed_line.split(",", 2))
        self._corners.append((x, y))
        return parsed_line


def reckon_area(rectangle: tuple[tuple[int, int], tuple[int, int]]):
    (x1, y1), (x2, y2) = rectangle
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


class D09Step1Puzzle(D09Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        # Find best area from all combinations
        best_area = 0
        for p1, p2 in combinations(self._corners, 2):
            area = reckon_area((p1, p2))
            if area > best_area:
                best_area = area

        return best_area


def flood_fill(borders: set[tuple[int, int]], internal_point: tuple[int, int]) -> set[tuple[int, int]]:
    directions = [OFFSETS[d] for d in CARDINAL_DIRS]
    visited: set[tuple[int, int]] = set()
    queue = deque([internal_point])
    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        x, y = current
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) not in borders:
                queue.append((new_x, new_y))
    return visited


def rectangle_inside(p1: tuple[int, int], p2: tuple[int, int], polygon: set[tuple[int, int]]):
    x1, y1 = p1
    x2, y2 = p2
    x_min, x_max = sorted((x1, x2))
    y_min, y_max = sorted((y1, y2))
    for x in range(x_min, x_max + 1):
        if (x, y_min) not in polygon or (x, y_max) not in polygon:
            return False
    return all(not ((x_min, y) not in polygon or (x_max, y) not in polygon) for y in range(y_min, y_max + 1))


class D09Step2Puzzle(D09Puzzle):
    def solve(self, flood_seed: tuple[int, int]) -> int:  # type: ignore
        # Flood fill polygon to get all points
        inside = flood_fill(self._borders, flood_seed)
        all_points = self._borders | inside
        # plot_points(all_points)

        # Find best area from all combinations
        best_area = 0
        for i, p1 in enumerate(self._compressed):
            for j, p2 in enumerate(self._compressed):
                if j <= i:
                    continue
                area = reckon_area((self._corners[i], self._corners[j]))
                if area <= best_area:
                    continue
                if rectangle_inside(p1, p2, all_points):
                    best_area = area
        return best_area
